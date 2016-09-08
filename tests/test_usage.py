#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import numpy as np
from ctmatching import psm, grouper, load_re78

#--- Minimum Usage ---
control = np.array([[10., 0., 7.], [1., 4., 8.],])
treatment = np.array([[8., 3., 8.], [2., -3., 4.],])
      
# by default, use_col = None, stratify_order = None, independent = True, k = 1
selected_control_index, selected_control_index_for_each_treatment = psm(control, treatment)

for treatment_sample, control_samples in grouper(
    control, treatment, selected_control_index_for_each_treatment):
    
    print("\n--- %s ---" % treatment_sample)
    print("--- match:")
    for control_sample in control_samples:
        print("    %s" % control_sample)
        
# use stratified order
selected_control_index, selected_control_index_for_each_treatment = psm(
    control, treatment, stratify_order=[[2], [0, 1]])
      
for treatment_sample, control_samples in grouper(
    control, treatment, selected_control_index_for_each_treatment):
    
    print("\n--- %s ---" % treatment_sample)
    print("--- match:")
    for control_sample in control_samples:
        print("    %s" % control_sample)
     
# Advance Usage
control, treatment = load_re78()
     
# we only use second, third, ... , 7th column and use third column (second of use_col)
# as the dominate feature, then 5th column as second dominate
selected_control_index, selected_control_index_for_each_treatment = psm(
    control, treatment, 
    use_col = [2,3,4,5,6,7], 
    stratify_order = [[1],[3],[0,2,4],[5]], 
    independent = False, 
    k = 2,
)
     
for treatment_sample, control_samples in grouper(
    control, treatment, selected_control_index_for_each_treatment):
     
    print("\n--- %s ---" % treatment_sample)
    print("--- match:")
    for control_sample in control_samples:
        print("    %s" % control_sample)