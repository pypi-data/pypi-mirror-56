extern crate rayon;

use rayon::prelude::*;

use std::borrow::BorrowMut;
use std::collections::BTreeMap;
use std::collections::BTreeSet;
use std::ops::Bound::{Excluded, Included, Unbounded};
use std::{mem, slice, time};

use log::{error, info, trace, warn, debug};

type Feat = i32;
type Diag = i32;
type Obs = usize;

#[repr(C)]
pub struct PyShape {
    rows: usize,
    cols: usize,
}

#[repr(C)]
pub struct PyArray<T> {
    len: usize,
    vec: *const T,
}

#[repr(C)]
pub struct PyBasicCsrMatrix {
    shape: PyShape,
    indices: PyArray<i32>,
    indptr: PyArray<i32>,
}

fn parse_basic_csr(csr_matrix: PyBasicCsrMatrix) -> (PyShape, &'static [i32], &'static [i32]) {
    let shape = csr_matrix.shape;
    let indices = csr_matrix.indices;
    let indptr = csr_matrix.indptr;
    let indices = unsafe { slice::from_raw_parts(indices.vec, indices.len) };
    let indptr = unsafe { slice::from_raw_parts(indptr.vec, indptr.len) };
    return (shape, indices, indptr);
}

fn obsdiag2feat(obs: usize, x_indptr: &'static [i32], x_indices: &'static [i32],
                feature_diagnoses: &BTreeMap<Feat, BTreeSet<Diag>>)
                -> Vec<Feat> {

    trace!("obsdiag2feat");

    // result vec of feature indicies belonging to obs
    let mut result = vec![];

    // track diagnoses-to-map
    let mut diag2map : BTreeSet<Diag> = BTreeSet::new();
    for diag in x_indptr[obs]..x_indptr[obs+1] {
        diag2map.insert(x_indices[diag as usize]);
    }

    // all zero?
    while diag2map.len() > 0 {
        // find a feature
        let mut all_processed = true;
        'inner: for &feat in feature_diagnoses.keys() {
            let featdiag_set = &feature_diagnoses[&feat];
            // all feature diagnoses in diag2map?
            if featdiag_set.is_subset(&diag2map) {
                for diag in featdiag_set {
                    diag2map.remove(diag);
                }
                // save to result
                trace!("Obs {} [{:?}]: saving {} [{:?}].",
                       obs, diag2map, feat, featdiag_set);
                result.push(feat as i32);
                all_processed = false;
                break 'inner;          // break out of for-loop
            }
        }

        if all_processed {
            // reaching that point means, that we do not have found a
            // single candidate for the remaining diagnoses, so we are
            // done => break out of while-loop
            break;
        }
    }

    return result;
}


fn obsdiag2featset(obs: usize, x_indptr: &'static [i32], x_indices: &'static [i32],
                   feature_diagnoses: &BTreeMap<Feat, BTreeSet<Diag>>)
                   -> BTreeSet<Feat> {

    // result set of feature indicies belonging to obs
    let mut result : BTreeSet<Feat> = BTreeSet::new();

    // track diagnoses-to-map
    let mut diag2map : BTreeSet<Diag> = BTreeSet::new();
    for diag in x_indptr[obs]..x_indptr[obs+1] {
        diag2map.insert(x_indices[diag as usize]);
    }

    trace!("obsdiag2featset: obs {} input feats: {:?}",
           obs, diag2map);

    // all zero?
    while diag2map.len() > 0 {
        // find a feature
        let mut all_processed = true;
        'inner: for &feat in feature_diagnoses.keys() {
            let featdiag_set = &feature_diagnoses[&feat];
            // all feature diagnoses in diag2map?
            if featdiag_set.is_subset(&diag2map) {
                for diag in featdiag_set {
                    diag2map.remove(diag);
                }
                // save to result
                trace!("obs {}: sav. out-feat {} [w/in-feats {:?}], \
                        rem. in-feats: {:?}",
                       obs, feat, featdiag_set, diag2map);
                result.insert(feat);
                all_processed = false;
                break 'inner;          // break out of for-loop
            }
        }

        if all_processed {
            // reaching that point means, that we do not have found a
            // single candidate for the remaining diagnoses, so we are
            // done => break out of while-loop
            break;
        }
    }

    trace!("obs {}: out-feats: {:?}", obs, result);
    return result;
}


fn alternative_features(feature_diagnoses: &BTreeMap<Feat, BTreeSet<Diag>>,
                        source_feature: &Feat)
                        -> BTreeSet<Feat> {
    // map source_feature from feature_diagnoses onto lower order
    // (splitted) features, so that the diagnose set remains intact
    // (if possible)

    let mut target_features : BTreeSet<Feat> = BTreeSet::new();
    let mut diag2map : BTreeSet<Diag> = feature_diagnoses.get(source_feature).unwrap().clone();

    let lower_features = feature_diagnoses.range((Excluded(source_feature), Unbounded));

    while diag2map.len() > 0 {
        let mut all_processed = true;
        'inner:
        for (&feat, &ref feat_diags) in lower_features.clone() {
            if feat_diags.is_subset(&diag2map) {
                for diag in feat_diags {
                    diag2map.remove(diag);
                }
                target_features.insert(feat);
                all_processed = false;
                break 'inner;
            }
        }
        if all_processed {
            break;
        }
    }
    return target_features;
}


#[no_mangle]
pub extern "C" fn remap_rows(x: PyBasicCsrMatrix, i: PyBasicCsrMatrix) -> PyBasicCsrMatrix {
    // We create a new (binary) Nxm sparse matrix out of the (binary)
    // Nxn design matrix X using the (binary) mxn indicator matrix I.
    // n...number of input features, m...number of output features,
    // N...number of observations.

    let begin = time::Instant::now();

    let (x_shape, x_indices, x_indptr) = parse_basic_csr(x);
    assert!(x_shape.rows == x_indptr.len()-1);

    let (i_shape, i_indices, i_indptr) = parse_basic_csr(i);
    assert!(i_shape.rows == i_indptr.len()-1);

    let n_obs = x_shape.rows;
    let n_in_feat = x_shape.cols;
    assert!(n_in_feat == i_shape.cols);
    let n_out_feat = i_shape.rows;

    // // count input feature cardinalities
    // println!("Counting input feature cardinalities...");
    // let mut in_card : Vec<u32> = vec![0; n_in_feat];
    // for obs in 0..n_obs {
    //     for idx in x_indptr[obs]..x_indptr[obs+1] {
    //         in_card[x_indices[idx as usize] as usize] += 1;
    //     }
    // }
    // println!("{:?}", in_card);

    // building map of features to diagnoses
    let mut feature_diagnoses : BTreeMap<Feat, BTreeSet<Diag>> = BTreeMap::new();

    // count output feature (pre-mapping) cardinalities
    for feat in 0..n_out_feat {
        let featidx = feat as Feat;
        feature_diagnoses.insert(featidx,
                                 (i_indptr[feat]..i_indptr[feat+1])
                                 .map(|i| i_indices[i as usize])
                                 .collect());
    }

    // println!("{:?}", feature_diagnoses);

    info!("Mapping {} patients onto {} features...", n_obs, n_out_feat);
    let mapped_obs = (0..n_obs)
        .into_par_iter()
        .map(|obs|
             obsdiag2feat(obs, x_indptr, x_indices, &feature_diagnoses));

    // build result vectors
    let mut mapped_indices : Vec<i32> = vec![];
    let mut mapped_indptr : Vec<i32> = vec![0];

    for obs in mapped_obs.collect::<Vec<Vec<i32>>>() {
        for o in obs {
            mapped_indices.push(o);
        }
        mapped_indptr.push(mapped_indices.len() as i32);
    }


    // the output sparse matrix
    let results = PyBasicCsrMatrix {
        shape: PyShape {
            rows: n_obs,
            cols: n_out_feat
        },
        indices: PyArray::<i32> {
            len: mapped_indices.len(),
            vec: mapped_indices.as_ptr()
        },
        indptr: PyArray::<i32> {
            len: mapped_indptr.len(),
            vec: mapped_indptr.as_ptr()
        }
    };

    mem::forget(mapped_indices);
    mem::forget(mapped_indptr);

    trace!(" completed in {} s.", begin.elapsed().as_secs());

    return results;
}


#[no_mangle]
pub extern "C" fn remap_rows_smin_obsolete(x: PyBasicCsrMatrix,
                                           i: PyBasicCsrMatrix,
                                           smin: u32)
                                           -> PyBasicCsrMatrix {

    let begin = time::Instant::now();

    // remap the rows while maintaining smin support per output feature
    let (x_shape, x_indices, x_indptr) = parse_basic_csr(x);
    assert!(x_shape.rows == x_indptr.len()-1);

    let (i_shape, i_indices, i_indptr) = parse_basic_csr(i);
    assert!(i_shape.rows == i_indptr.len()-1);

    let n_obs = x_shape.rows;
    let n_in_feat = x_shape.cols;
    assert!(n_in_feat == i_shape.cols);
    let n_out_feat = i_shape.rows;

    // building map of features to diagnoses
    let mut feature_diagnoses : BTreeMap<Feat, BTreeSet<Diag>> = BTreeMap::new();
    for feat in 0..n_out_feat {
        let featidx = feat as Feat;
        feature_diagnoses.insert(featidx,
                                 (i_indptr[feat]..i_indptr[feat+1])
                                 .map(|i| i_indices[i as usize])
                                 .collect());
    }

    // building map of diagnoses to observations
    let mut obs_diagnoses : BTreeMap<Obs, BTreeSet<Diag>> = BTreeMap::new();
    for obs in 0..n_obs {
        obs_diagnoses.insert(obs,
                             (x_indptr[obs]..x_indptr[obs+1])
                             .map(|i| x_indices[i as usize])
                             .collect());
    }

    info!("Mapping {} patients onto {} features while maintaining {} support...",
          n_obs, n_out_feat, smin);

    trace!("Mapping matrix (output feat: input feats):");
    trace!("{:?}", feature_diagnoses);

    // obs_features : this is what we return to the caller, the
    // observations mapped to feature sets.
    let mut obs_features : BTreeMap<Obs, BTreeSet<Feat>> = (0..n_obs)
        .into_par_iter()
        .map(|obs|
             (obs, obsdiag2featset(obs, x_indptr, x_indices, &feature_diagnoses)))
        .collect();

    let mut feature_obs : BTreeMap<Feat, BTreeSet<Obs>> = BTreeMap::new();

    // TODO: understand this is really a strange construct
    for (&obs, &ref feats) in &obs_features {
        for &feat in feats {
            if feature_obs.contains_key(&feat) {
                if let Some(obs_set) = feature_obs.get_mut(&feat) {
                    obs_set.insert(obs);
                } else {
                    panic!("feature {} has no observation set.", feat);
                }
            } else {
                let mut obs_set : BTreeSet<Obs> = BTreeSet::new();
                obs_set.insert(obs);
                feature_obs.borrow_mut().insert(feat, obs_set);
            }
        }
    }

    trace!("feature_obs: {:?}", feature_obs);

    // count the feature-support
    let mut feat_count : BTreeMap<Feat, usize> = feature_obs
        .iter()
        .map(|(feat, obs_set)| (*feat, obs_set.len()))
        .collect();
    // println!("feat_count: {:?}", feat_count);

    trace!("feat_count: {:?}", feat_count);

    // we loop over all features : the support count can only change
    // _below_ the remapped feature, thus we can safely go over from
    // top to bottom once:
    let mut candidate_feat : Feat = 0;

    trace!("looping...");

    loop {

        // find (to remove) FIRST feature coming after (including) the
        // candidate, where count < smin
        let invalid_feat : Option<Feat> = {
            if let Some((&x,_)) = feature_diagnoses
            // if let Some(&x) = feature_diagnoses
                // .keys()
                // .find(|&feat| *feat_count.get(&feat).unwrap_or(&0) < smin as usize) {
                .range((Included(candidate_feat), Unbounded))
                .find(|(&feat, _)| *feat_count.get(&feat).unwrap_or(&0) < smin as usize) {
                    Some(x)
                } else {
                    None
                }
        };

        if let Some(feat) = invalid_feat {

            // first, we find the features that we should map instead
            // of the to-be-removed feature:
            let alt_features = alternative_features(&feature_diagnoses, &feat);
            trace!("Alternatives for feature {} are: {:?}.", feat, alt_features);

            // then, we actually remove the feature from
            // feature_diagnoses and from feature_obs:
            let obs2remap = {
                trace!("Removing feat {} with {} obs [len={}]",
                       feat, feat_count.get(&feat).unwrap_or(&0), feature_diagnoses.len());

                let _diags2remap = feature_diagnoses.remove(&feat);
                let obs2remap = feature_obs.remove(&feat);

                trace!("Remapping patients with diagnoses {:?}: {:?}.", _diags2remap, obs2remap);

                obs2remap.unwrap_or(BTreeSet::new())
            };

            // then, we update feature_obs
            for alt_feat in alt_features.iter() {
                if !feature_obs.contains_key(alt_feat) {
                    feature_obs.insert(*alt_feat, BTreeSet::new());
                }
                if let Some(obs_set) = feature_obs.get_mut(alt_feat) {
                    obs_set.append(&mut obs2remap.clone());
                } else {
                    panic!("feature {} has no observations set.", alt_feat);
                }
            }

            // then, we update obs_features (our results!!!)
            {
                let n_obs2remap = obs2remap.len();
                for obs in obs2remap {
                    let obs_feats = obs_features.get_mut(&obs).unwrap();
                    trace!("Update obs {} / feat {}: {:?}", obs, feat, obs_feats);
                    obs_feats.remove(&feat);
                    obs_feats.append(&mut alt_features.clone());

                    trace!(" -> {:?}.", obs_feats);
                }

                // and we update the feature counts
                assert_eq!(*feat_count.get(&feat).unwrap_or(&0), n_obs2remap);
                feat_count.remove(&feat);
                for feat in alt_features.iter() {
                    if !feat_count.contains_key(feat) {
                        feat_count.insert(*feat, 0);
                    }
                    if let Some(x) = feat_count.get_mut(&feat) { *x += n_obs2remap; }
                    else { panic!("feature {} has no observations set.", feat); }
                }
            }

            if (feat as usize) < n_out_feat-1 {
                // update the candidate
                candidate_feat = feat + 1;
            } else {
                break;
            }


        } else {
            // no features removed => break out of loop
            break;
        }
    }

    trace!("mapping complete");

    // build result vectors : the result must be based on the original
    // index values
    let mut mapped_indices : Vec<i32> = vec![];
    let mut mapped_indptr : Vec<i32> = vec![0];

    for (_obs, feats) in &obs_features {
        for feat in feats {
            mapped_indices.push(*feat);
        }
        mapped_indptr.push(mapped_indices.len() as i32);
    }


    // the output sparse matrix
    let results = PyBasicCsrMatrix {
        shape: PyShape {
            rows: n_obs,
            cols: n_out_feat
        },
        indices: PyArray::<i32> {
            len: mapped_indices.len(),
            vec: mapped_indices.as_ptr()
        },
        indptr: PyArray::<i32> {
            len: mapped_indptr.len(),
            vec: mapped_indptr.as_ptr()
        }
    };

    mem::forget(mapped_indices);
    mem::forget(mapped_indptr);

    trace!(" completed in {} s.", begin.elapsed().as_secs());

    // {
    //     let updated_feat_count : BTreeMap<Feat, usize> = feature_obs
    //         .iter()
    //         .map(|(feat, obs_set)| (*feat, obs_set.len()))
    //         .collect();
    //     assert_eq!(feat_count, updated_feat_count);

    //     assert_eq!(updated_feat_count.iter().all(|(feat, count)| *count >= smin as usize), true);

    //     // println!("Asserted final feature counts: {:?}.", feat_count);
    // }

    // {
    //     // re-compute feature_obs from obs_features and compare with
    //     // acutal version
    //     let mut updated_feature_obs : BTreeMap<Feat, BTreeSet<Obs>> = BTreeMap::new();

    //     for (&obs, &ref feats) in &obs_features {
    //         for &feat in feats {
    //             if updated_feature_obs.contains_key(&feat) {
    //                 if let Some(obs_set) = updated_feature_obs.get_mut(&feat) {
    //                     obs_set.insert(obs);
    //                 }
    //             } else {
    //                 let mut obs_set : BTreeSet<Obs> = BTreeSet::new();
    //                 obs_set.insert(obs);
    //                 updated_feature_obs.borrow_mut().insert(feat, obs_set);
    //             }
    //         }
    //     }

    //     let feature_obs_counts = feature_obs.iter().map(|(feat, obs)| (*feat, obs.len()))
    //         .collect::<BTreeMap<_,_>>();
    //     assert_eq!(feature_obs_counts, feat_count);
    //     assert_eq!(updated_feature_obs.iter().map(|(feat, obs)| (*feat, obs.len()))
    //                .collect::<BTreeMap<_,_>>(), feature_obs_counts);
    // }


    return results;
}


#[no_mangle]
pub extern "C" fn remap_rows_smin(x: PyBasicCsrMatrix,
                                  i: PyBasicCsrMatrix,
                                  smin: u32)
                                  -> PyBasicCsrMatrix {

    let begin = time::Instant::now();

    // remap the rows while maintaining smin support per output feature
    let (x_shape, x_indices, x_indptr) = parse_basic_csr(x);
    assert!(x_shape.rows == x_indptr.len()-1);

    let (i_shape, i_indices, i_indptr) = parse_basic_csr(i);
    assert!(i_shape.rows == i_indptr.len()-1);

    let n_obs = x_shape.rows;
    let n_in_feat = x_shape.cols;
    assert!(n_in_feat == i_shape.cols);
    let n_out_feat = i_shape.rows;

    // building map of features to diagnoses
    let mut feature_diagnoses : BTreeMap<Feat, BTreeSet<Diag>> = BTreeMap::new();
    for feat in 0..n_out_feat {
        let featidx = feat as Feat;
        feature_diagnoses.insert(featidx,
                                 (i_indptr[feat]..i_indptr[feat+1])
                                 .map(|i| i_indices[i as usize])
                                 .collect());
    }

    // building map of diagnoses to observations
    let mut obs_diagnoses : BTreeMap<Obs, BTreeSet<Diag>> = BTreeMap::new();
    for obs in 0..n_obs {
        obs_diagnoses.insert(obs,
                             (x_indptr[obs]..x_indptr[obs+1])
                             .map(|i| x_indices[i as usize])
                             .collect());
    }

    info!("Mapping {} patients onto {} features while maintaining {} support...",
          n_obs, n_out_feat, smin);

    trace!("Mapping matrix (output feat: input feats):");
    trace!("{:?}", feature_diagnoses);

    // obs_features : this is what we return to the caller, the
    // observations mapped to feature sets.
    let mut obs_features : BTreeMap<Obs, BTreeSet<Feat>> = (0..n_obs)
        .into_par_iter()
        .map(|obs|
             (obs, obsdiag2featset(obs, x_indptr, x_indices, &feature_diagnoses)))
        .collect();

    trace!("obs_features: {:?}", obs_features);

    let mut feature_obs : BTreeMap<Feat, BTreeSet<Obs>> = BTreeMap::new();

    // TODO: understand this is really a strange construct
    for (&obs, &ref feats) in &obs_features {
        for &feat in feats {
            if feature_obs.contains_key(&feat) {
                if let Some(obs_set) = feature_obs.get_mut(&feat) {
                    obs_set.insert(obs);
                } else {
                    panic!("feature {} has no observation set.", feat);
                }
            } else {
                let mut obs_set : BTreeSet<Obs> = BTreeSet::new();
                obs_set.insert(obs);
                feature_obs.borrow_mut().insert(feat, obs_set);
            }
        }
    }

    trace!("feature_obs: {:?}", feature_obs);

    // count the feature-support
    let mut feat_count : BTreeMap<Feat, usize> = feature_obs
        .iter()
        .map(|(feat, obs_set)| (*feat, obs_set.len()))
        .collect();

    trace!("feat_count: {:?}", feat_count);

    trace!("looping...");

    loop {

        // identifying features with support < smin and not support == 0
        let invalid_feat : Option<Feat> = {
            if let Some((&x,_)) = feature_diagnoses
                .iter()
                //.range((Included(0), Unbounded))
                .find(|(&feat, _)| {
                    let count = *feat_count.get(&feat).unwrap_or(&0);
                    ((count < smin as usize) & (count != 0))}) {
                    Some(x)
                } else {
                    None
                }
        };

        if let Some(feat) = invalid_feat {

            debug!("invalid_feat: {:?}", feat);

            // we find the patients with that (invalid) feature: all
            // of these need to be mapped again afresh

            // we actually remove the feature from
            // feature_diagnoses and from feature_obs:
            feature_diagnoses.remove(&feat);
            let obs2remap = feature_obs.remove(&feat).unwrap();


            // fix observation counts
            for obs in obs2remap.iter() {
                // first, we remove the old (invalid) features & fix the counts
                let old_obs_features = obs_features.remove(obs).unwrap();
                for old_feat in old_obs_features.iter() {
                    let old_feat_count = feat_count.remove(old_feat).unwrap();
                    if old_feat_count > 1 {
                        feat_count.insert(*old_feat, old_feat_count-1);
                    }
                    // fix feature_obs
                    if let Some(f) = feature_obs.get_mut(old_feat) {
                        f.remove(obs);
                    }
                }

                // then, we add the new ones
                let new_obs_features = obsdiag2featset(*obs,
                                                       x_indptr,
                                                       x_indices,
                                                       // v--- this is updated already
                                                       &feature_diagnoses);

                debug!("obs {}: feature update {:?} -> {:?}",
                       obs, old_obs_features, new_obs_features);

                // fix observation counts
                for new_feat in new_obs_features.iter() { // obs_features.get(obs).unwrap() {
                    // compute new count
                    let count = feat_count.remove(new_feat).unwrap_or(0) + 1;
                    // set new count
                    feat_count.insert(*new_feat, count);

                    // fix feature_obs
                    if let Some(f) = feature_obs.get_mut(new_feat) {
                        f.insert(*obs);
                    } else {
                        let mut set = BTreeSet::new();
                        set.insert(*obs);
                        feature_obs.insert(*new_feat, set);
                    }
                }

                obs_features.insert(*obs, new_obs_features);

                trace!("updated feat_obs: {:?}", feature_obs);
                trace!("updated feat_count: {:?}", feat_count);
            }

        } else {
            // no features removed => break out of loop
            break;
        }
    }

    debug!("mapping complete");
    // debug!("final (online) feature counts: {:?}", feat_count);

    // recount from feature_obs
    let feat_count_final : BTreeMap<Feat, usize> = feature_obs
        .iter()
        .map(|(feat, obs_set)| (*feat, obs_set.len()))
        .collect();

    let mut feat_count_delta : BTreeMap<Feat, i32> = BTreeMap::new();

    if feat_count != feat_count_final {
        debug!("final feature counts seem to mismatch");

        // compute differences
        for (&fin_f, &fin_c) in &feat_count_final {
            let c : usize = feat_count.remove(&fin_f).unwrap_or(0);
            if c != fin_c {
                // different counts here => add the difference back
                feat_count_delta.insert(fin_f, c as i32 - fin_c as i32);
            }
        }
        // iterate over (remaining) other counts
        for (other_f, other_c) in feat_count {
            let fin_c : usize = *feat_count_final.get(&other_f).unwrap_or(&0);
            if other_c != fin_c {
                // different counts here => add the difference back
                feat_count_delta.insert(other_f, other_c as i32 - fin_c as i32);
            }
        }

        if feat_count_delta.len() > 0 {
            error!("differences: {:?}", feat_count_delta);
            panic!("FINAL OUT-FEATURE-OBS COUNTS MISMATCH!");
        }
    }

    // build result vectors : the result must be based on the original
    // index values
    let mut mapped_indices : Vec<i32> = vec![];
    let mut mapped_indptr : Vec<i32> = vec![0];

    for (_obs, feats) in &obs_features {
        for feat in feats {
            mapped_indices.push(*feat);
        }
        mapped_indptr.push(mapped_indices.len() as i32);
    }


    // the output sparse matrix
    let results = PyBasicCsrMatrix {
        shape: PyShape {
            rows: n_obs,
            cols: n_out_feat
        },
        indices: PyArray::<i32> {
            len: mapped_indices.len(),
            vec: mapped_indices.as_ptr()
        },
        indptr: PyArray::<i32> {
            len: mapped_indptr.len(),
            vec: mapped_indptr.as_ptr()
        }
    };

    mem::forget(mapped_indices);
    mem::forget(mapped_indptr);

    trace!(" completed in {} s.", begin.elapsed().as_secs());

    return results;
}


#[no_mangle]
pub extern "C" fn init() {
    env_logger::init();
}


#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
