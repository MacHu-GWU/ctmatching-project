#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Control, treatment matching algorithm main module. (Propensity score matching)
"""

try:
    from .exc import InputError, NotEnoughControlSampleError
    from .orderedset import OrderedSet
except:
    from ctmatching.exc import InputError, NotEnoughControlSampleError
    from ctmatching.orderedset import OrderedSet

from sklearn import preprocessing
from sklearn.neighbors import DistanceMetric
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd


def normalize(train, test):
    """Pre-processing, normalize data by eliminating mean and variance.

    :param train: 2-d ndarray like data.
    :param test: 2-d ndarray like data.
    """
    scaler = preprocessing.StandardScaler().fit(
        train)  # calculate mean and variance
    train = scaler.transform(train)  # standardize train
    test = scaler.transform(test)  # standardize test
    return train, test


def dist(X, Y):
    """Calculate X, Y distance matrix.

    X, Y are M x N matrix. N must be same.

    :param X: 2-d ndarray like data.
    :param Y: 2-d ndarray like data.
    """
    distance_calculator = DistanceMetric.get_metric("euclidean")
    return distance_calculator.pairwise(X, Y)


def exam_input(control, treatment, stratify_order=None):
    """Exam input argument.
    """
    try:
        control_sample = control[0]
        treatment_sample = treatment[0]
    except:
        raise InputError("control/treatment syntax error!")

    if len(control_sample) != len(treatment_sample):
        raise InputError(
            "control sample and treatment sample are different in size!")

    if stratify_order:
        for chunk in stratify_order:
            if len(chunk) != len(set(chunk)):
                raise InputError(
                    "duplicate column index is not allowed in one order!")

            for index in chunk:
                if index not in range(len(control_sample)):
                    raise InputError("column index is out of range!")


#--- Matching ---
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

    :param stratify_order:
    :returns nn_index: knn index, M1 X M2 matrix. M1 is number of treatment, M2
      is number of control.
    """
    exam_input(control, treatment, stratify_order)
    treatment_std, control_std = normalize(treatment, control)

    distmatrix_list = list()
    nn_index = list()

    for stratify_index in stratify_order:
        sub_control = control_std[:, stratify_index]
        sub_treatment = treatment_std[:, stratify_index]
        distmatrix = dist(sub_treatment, sub_control)
        distmatrix_list.append(distmatrix)

    for chunk in zip(*distmatrix_list):
        df = pd.DataFrame(np.array(chunk).T)
        nn_index.append(
            df.sort(columns=list(range(len(stratify_order)))).index.values)

    nn_index = np.array(nn_index)

    return nn_index


def non_stratified_matching(control, treatment):
    """Find index of KNN-neighbor of control sample for treatment group.

    :returns nn_index: knn index, M1 X M2 matrix. M1 is number of treatment, M2
      is number of control.

    Conponent function of :func:`psm`. 
    """
    exam_input(control, treatment)
    treatment_std, control_std = normalize(treatment, control)

    nbrs = NearestNeighbors(
        n_neighbors=len(control_std), algorithm="kd_tree").fit(control_std)
    _, nn_index = nbrs.kneighbors(treatment_std)
    return nn_index


#--- Selection ---
def non_repeat_index_matching(nn_indices, k=1):
    """All treatment samples match against different samples from control group.

    For example::

    - treatment_sample1 matches: control_1, control_25, control_30
    - treatment_sample2 matches: control_2, control_25, control_34

    Because treatment_sample1 already took control_25, so treatment_sample2 has
    to take control2 and control_34 (second nearest, third nearest).

    :returns selected_control_index: all control sample been selected for 
      entire treatment group.
    :returns selected_control_index_for_each_treatment: selected control sample
      for each treatment sample.

    Conponent function of :func:`psm`.
    """
    num_of_control = len(nn_indices[0])
    num_of_treatment = len(nn_indices)

    if k * num_of_treatment > num_of_control:
        raise InputError(
            ("There's no enough samples in control group to "
             "perform non repeat matching. Use independent "
             "matching instead."))

    # initial all selected control group sample indices
    selected_control_index = OrderedSet(list())
    selected_control_index_for_each_treatment = list()
    for indice in nn_indices:  # for indice that tr1 -> [4, 11, 6, 7, ...]
        counter = 0
        selected = list()
        for ind in indice:
            if ind not in selected_control_index:  # if has not been selected
                selected_control_index.add(ind)
                selected.append(ind)
                counter += 1
                # if already selected k control sample, then stop
                if counter == k:
                    break
        selected_control_index_for_each_treatment.append(selected)

    selected_control_index = np.array(list(selected_control_index))
    selected_control_index_for_each_treatment = np.array(
        selected_control_index_for_each_treatment)

    return selected_control_index, selected_control_index_for_each_treatment


def independent_index_matching(nn_indices, k=1):
    """Each treatment_sample match against to first k nearest neighbor 
    in control group. Multiple treatment sample may match the same control 
    sample.

    :returns selected_control_index: all control sample been selected for 
      entire treatment group.
    :returns selected_control_index_for_each_treatment: selected control sample
      for each treatment sample.

    Conponent function of :func:`psm`. 
    """
    selected_control_index_for_each_treatment = nn_indices[:, list(range(k))]
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

    :param control: control group sample data, m1 x n matrix. Example::

        [[c1_1, c1_2, ..., c1_n], # c means control
         [c2_1, c2_2, ..., c2_n],
         ...,
         [cm1_1, cm1_2, ..., cm1_n],]

    :type control: numpy.ndarray
    :param treatment: control group sample data, m2 x n matrix. Example::

        [[t1_1, t1_2, ..., t1_n], # t means treatment
         [t2_1, t2_2, ..., t2_n],
         ...,
         [tm1_1, tm1_2, ..., tm1_n],]

    :type treatment: numpy.ndarray
    :param use_col: (default None, use all) list of column index. Example::

        [0, 1, 4, 6, 7, 9] # use first, second, fifth, ... columns

    :type use_col: list or numpy.ndarray

    :param stratify_order: (default None, use normal nearest neighbor) 
      list of list. Example::

        # for input data has 6 columns
        # first feature has highest priority
        # [second, third, forth] features' has second highest priority by mean of euclidean distance
        # fifth feature has third priority, ...
        [[0], [1, 2, 3], [4], [5]]

    :type stratify_order: list of list

    :param independent: (default True), if True, same treatment sample could be
      matched to different control sample.
    :type independent: boolean

    :param k: (default 1) Number of samples selected from control group.
    :type k: int

    :returns selected_control_index: all control sample been selected for 
      entire treatment group.
    :returns selected_control_index_for_each_treatment: selected control sample
      for each treatment sample.

    selected_control_index: selected control sample index. Example (k = 3)::

        (m2 * k)-length array: [7, 120, 43, 54, 12, 98, ..., 71, 37, 14]

    selected_control_index_for_each_treatment: selected control sample index for 
    each treatment sample. Example (k = 3)::

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

    # select useful columns
    if use_col:
        control_used = control[:, use_col].astype(float)
        treatment_used = treatment[:, use_col].astype(float)
    else:
        control_used, treatment_used = control, treatment

    # knn-match
    if stratify_order:
        nn_index = stratified_matching(
            control_used, treatment_used, stratify_order)
    else:
        nn_index = non_stratified_matching(control_used, treatment_used)

    # select paired
    if independent:
        (
            selected_control_index,
            selected_control_index_for_each_treatment,
        ) = independent_index_matching(nn_index, k)
    else:
        (
            selected_control_index,
            selected_control_index_for_each_treatment,
        ) = non_repeat_index_matching(nn_index, k)

    return selected_control_index, selected_control_index_for_each_treatment


def grouper(control, treatment, selected_control_index_for_each_treatment):
    """Generate treatment sample and matched control samples pair.
    """
    control, treatment = np.array(control), np.array(treatment)
    for treatment_sample, index in zip(
            treatment, selected_control_index_for_each_treatment):
        control_samples = control[index]
        yield treatment_sample, control_samples
