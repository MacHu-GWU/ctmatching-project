#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from ctmatching import psm, load_re78
import numpy as np

if __name__ == "__main__":
    """
    Minimal Usage
    """
    control = np.array([[10., 0., 7.], [1., 4., 8.],])
    treatment = np.array([[8., 3., 8.], [2., -3., 4.],])
     
    # by default, use_col = None, stratify_order = None, independent = True, k = 1
    selected_control, selected_control_each_treatment = psm(
        control, treatment)
     
    for treatment_sample, index in zip(treatment, selected_control_each_treatment):
        print("%s matches %s" % (treatment_sample, control[index]))
         
    selected_control, selected_control_each_treatment = psm(
        control, treatment, stratify_order=[[2], [0, 1]])
     
    for treatment_sample, index in zip(treatment, selected_control_each_treatment):
        print("%s matches %s" % (treatment_sample, control[index]))
    
    """
    Advance Usage
    """
    control, treatment = load_re78()
    
    # we only use second, third, ... , 7th column and use third column (second of use_col)
    # as the dominate feature, then 5th column as second dominate
    selected_control, selected_control_each_treatment = psm(
        control, treatment, use_col=[1,2,3,4,5,6], stratify_order=[[1],[3],[0,2,4],[5]], 
        independent=False, k=2)
        
    for treatment_sample, index in zip(treatment, selected_control_each_treatment):
        print("=======================================")
        print(treatment_sample.tolist())
        print("matches")
        for sample in control[index].tolist():
            print(sample)