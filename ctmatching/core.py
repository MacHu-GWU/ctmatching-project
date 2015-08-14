#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Control, treatment matching algorithm main module. (Propensity score matching)         

About
~~~~~

**Copyright (c) 2015 by Sanhe Hu**

- Author: Sanhe Hu
- Email: husanhe@gmail.com
- Lisence: MIT


**Compatibility**

- Python2: Yes
- Python3: Yes
    

class, method, func, exception
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from __future__ import print_function
from ctmatching.exc import InputError, NotEnoughControlSampleError
from ctmatching.orderedset import OrderedSet
from sklearn import preprocessing
from sklearn.neighbors import DistanceMetric
from sklearn.neighbors import NearestNeighbors
import numpy as np, pandas as pd

def normalize(train, test):
    """Pre-processing, normalize data by eliminating mean and variance.
    """
    scaler = preprocessing.StandardScaler().fit(train) # calculate mean and variance
    train = scaler.transform(train) # standardize train
    test = scaler.transform(test) # standardize test
    return train, test

def dist(X, Y):
    """Calculate X, Y distance matrix.
    """
    distance_calculator = DistanceMetric.get_metric("euclidean")
    return distance_calculator.pairwise(X, Y)

def exam_input(control, treatment, stratify_order=None):
    """Exam input argument.
    """
    try:
        control_sample = control[0]
        treatment_sample = treatment[0]
        if len(control_sample) != len(treatment_sample):
            raise InputError
    except InputError as e:
        raise e("control group and treatment group has different dimension.")
    except:
        raise InputError("control/treatment syntax error")
    
    if stratify_order:
        try:
            column_index = set()
            for chunk in stratify_order:
                for index in chunk:
                    column_index.add(index)
            if column_index != set(range(len(control_sample))):
                raise InputError(
                "stratify_order syntax error, please read doc for more info.")
        except:
            raise InputError(
                "stratify_order syntax error, please read doc for more info.")

############
# Matching #
############

def stratified_matching(control, treatment, stratify_order):
    """Calculate the order of matched control samples. Conponent function of 
    :func:`psm`. 
    
    Here's how it's done.
    
    ::
    
        control = 1000 * 5 (1000 samples, 5-dimension vector)
        treatment = 100 * 5 (100 samples, 5-dimension vector)
        stratify_order = [[0], [1,2,3], [4]]
    
    1. construct 3 distance matrix for 3 stratify rules, each matrix size is 
    100 * 1000
    
        - select first column of treatment
        - select first column of control
        - compute distance matrix
        - repeat this over three order
    
    2. construct a 1000 * 3 matrix, each column is the distance array against 
    control then sort them by first column, then second column, finally third 
    column. now first row index should be the nearest sample in control group 
    by mean of stratification. append the row index to "indices" matrix.
    """
    exam_input(control, treatment, stratify_order)
    treatment_std, control_std = normalize(treatment, control)

    distmatrix_list = list()
    indices = list()
    
    for stratify_index in stratify_order:
        sub_control = control_std[:, stratify_index]
        sub_treatment = treatment_std[:, stratify_index]
        distmatrix = dist(sub_treatment, sub_control)
        distmatrix_list.append(distmatrix)

    for chunk in zip(*distmatrix_list):
        df = pd.DataFrame(np.array(chunk).T)
        indices.append(
            df.sort(columns=list(range(len(stratify_order)))).index.values)

    return np.array(indices)

def non_stratified_matching(control, treatment):
    """Simply calculate knn index for each treatment sample. Conponent function 
    of :func:`psm`. 
    """
    exam_input(control, treatment)
    treatment_std, control_std = normalize(treatment, control)

    nbrs = NearestNeighbors(n_neighbors=len(control_std), algorithm="kd_tree").fit(control_std)
    _, indices = nbrs.kneighbors(treatment_std)
    return indices

#############
# Selection #
#############

def non_repeat_index_matching(indices, k=1):
    """All treatment samples match against different samples from control group.
    Conponent function of :func:`psm`.
    
    For example::
    
        treatment_sample1 matches control_1, control_25, control_30
        treatment_sample2 matches control_2, control_25, control_34
    
    Because treatment_sample1 already took control_25, so treatment_sample2 has
    to take control2 and control_34 (second nearest, third nearest).
    """
    num_of_control = len(indices[0])
    num_of_treatment = len(indices)
    
    if k * num_of_treatment > num_of_control:
        raise NotEnoughControlSampleError(
            ("There's no enough samples in control group to "
             "perform non repeat matching. Use independent "
             "matching instead."))
    
    
    selected_control_index = OrderedSet(list()) # initial all selected control group sample indices
    selected_control_index_for_each_treatment = list()
    for indice in indices: # for indice that tr1 -> [4, 11, 6, 7, ...]
        counter = 0
        selected = list()
        for ind in indice:
            if ind not in selected_control_index: # if has not been selected
                selected_control_index.add(ind)
                selected.append(ind)
                counter += 1
                if counter == k: # if already selected k control sample, then stop
                    break
        selected_control_index_for_each_treatment.append(selected)
    
    selected_control_index = np.array(list(selected_control_index))
    selected_control_index_for_each_treatment = np.array(selected_control_index_for_each_treatment)
    
    return selected_control_index, selected_control_index_for_each_treatment

def independent_index_matching(indices, k=1):
    """Each treatment_sample match against to first k nearest neighbor 
    in control group. Multiple treatment sample may match the same control 
    sample.
    
    Conponent function of :func:`psm`. 
    """
    selected_control_index_for_each_treatment = indices[:, list(range(k))]
    selected_control_index = list()
    for indice in selected_control_index_for_each_treatment:
        for ind in indice:
            selected_control_index.append(ind)
    selected_control_index = np.array(selected_control_index)
    
    return selected_control_index, selected_control_index_for_each_treatment

def psm(control, treatment, use_col=None, stratify_order=None, independent=True, k=1):
    """Propensity score matching main function.
    
    If you want to know the inside of the psm algorithm, check 
    :func:`stratified_matching`, :func:`non_stratified_matching`,
    :func:`non_repeat_index_matching`, :func:`independent_index_matching`.
    otherwise, just read the parameters' definition.
    
    Suppose we have m1 control samples, m2 treatment samples. Sample is 
    n-dimension vector.
    
    :param control: control group sample data, m1 x n matrix. Example:
    
    .. code-block:: python
    
        [[c1_1, c1_2, ..., c1_n], # c means control
         [c2_1, c2_2, ..., c2_n],
         ...,
         [cm1_1, cm1_2, ..., cm1_n],]
         
    :type control: numpy.ndarray
    :param treatment: control group sample data, m2 x n matrix. Example:
    
    .. code-block:: python
    
        [[t1_1, t1_2, ..., t1_n], # t means treatment
         [t2_1, t2_2, ..., t2_n],
         ...,
         [tm1_1, tm1_2, ..., tm1_n],]
         
    :type treatment: numpy.ndarray
    :param use_col: (default None, use all) list of column index. Example:
    
    .. code-block:: python
    
        [0, 1, 4, 6, 7, 9] # use first, second, fifth, ... columns
        
    :type use_col: list or numpy.ndarray
    
    :param stratify_order: (default None, use normal nearest neighbor) 
      list of list. Example:
    
    .. code-block:: python
    
        # for input data has 6 columns
        # first feature has highest priority
        # [second, third, forth] features' has second highest priority by mean of euclidean distance
        # fifth feature has third priority, ...
        [[0], [1, 2, 3], [4], [5]]
        
    :type stratify_order: list of list
    
    :param independent: (default True)
    :type independent: boolean
    
    :param k: (default 1) Number of samples selected from control group.
    :type k: int
    
    :return: selected_control_index, selected_control_index_for_each_treatment
    :rtype: tuple
    
    selected_control_index: selected control sample index. Example (k = 3):
    
    .. code-block:: python
        
        (m2 * k)-length array: [7, 120, 43, 54, 12, 98, ..., 71, 37, 14]
    
    selected_control_index_for_each_treatment: selected control sample index for 
    each treatment sample. Example (k = 3):
     
    .. code-block:: python
        
        # for treatment[0], we have control[7], control[120], control[43]
        # matched by mean of stratification.
        [[7, 120, 43],
         [54, 12, 98],
         ...,
         [71, 37, 14],]
         
    :raises InputError: if the input parameters are not legal.
    :raises NotEnoughControlSampleError: if don't have sufficient data for 
      independent index matching.
    """
    if not isinstance(control, np.ndarray):
        control = np.array(control)
    if not isinstance(treatment, np.ndarray):
        treatment = np.array(treatment)

    if use_col: # select useful columns
        control_used, treatment_used = control[:, use_col], treatment[:, use_col]
    else:
        control_used, treatment_used = control, treatment

    if stratify_order: # match phase
        indices = stratified_matching(control_used, treatment_used, stratify_order)
    else:
        indices = non_stratified_matching(control_used, treatment_used)
    
    if independent: # select phase
        selected_control_index, selected_control_index_for_each_treatment = independent_index_matching(indices, k)
    else:
        selected_control_index, selected_control_index_for_each_treatment = non_repeat_index_matching(indices, k)
        
    return selected_control_index, selected_control_index_for_each_treatment

if __name__ == "__main__":
    import unittest
    from testdata import load_re78
    
    def display_matching_result(control, treatment, selected_control_index_for_each_treatment):
        for treatment_sample, index in zip(treatment, selected_control_index_for_each_treatment):
            print("=====================================================================")
            print(treatment_sample)
            print("matches")
            for control_sample in control[index]:
                print(control_sample)

    class ControlTreatmentMatchingUnittest(unittest.TestCase):
        def test_exam_input(self):
            control, treatment = load_re78()
            control, treatment = control[:, list(range(1, 7))], treatment[:, list(range(1, 7))]
            stratify_order = [[1],[3],[0,2,4],[5]]
            exam_input(control, treatment, stratify_order) # pass exam
        
        
        def test_stratified_matching_and_none_repeat_index_matching(self):
            control, treatment = load_re78()
            control, treatment = control[:, list(range(1, 7))], treatment[:, list(range(1, 7))]
            stratify_order = [[1],[3],[0,2,4],[5]]
            
            indices = stratified_matching(control, treatment, stratify_order)
            selected_control_index, selected_control_index_for_each_treatment = non_repeat_index_matching(
                                                                                indices, 1)

            display_matching_result(control, treatment, selected_control_index_for_each_treatment)
        
        def test_non_stratified_matching_and_independent_index_matching(self):
            control, treatment = load_re78()
            control, treatment = control[:, list(range(1, 7))], treatment[:, list(range(1, 7))]
            indices = non_stratified_matching(control, treatment)
            selected_control_index, selected_control_index_for_each_treatment = independent_index_matching(
                                                                                indices, 1)

            display_matching_result(control, treatment, selected_control_index_for_each_treatment)
        
        def test_psm(self):
            control, treatment = load_re78()
            selected_control_index, selected_control_index_for_each_treatment = psm(
                control, treatment, [1,2,3,4,5,6], [[1],[3],[0,2,4],[5]], True, 1)
            
            display_matching_result(control, treatment, selected_control_index_for_each_treatment)
            
    unittest.main()    