#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ctmatching algoritm example data set loader.
"""

import pandas as pd
import os

def load_re78():
    """1978 US people earning data by race, age, gender, educations..
    
    429 control samples, 185 treatment samples. Each sample has 10 properties.
    
    Usage::
    
        >>> from ctmatching import load_re78
        >>> control, treatment = load_re78()
        >>> control.shape
        (429, 10)
        >>> treatment.shape
        (185, 10)
        
    description of this data: http://users.nber.org/~rdehejia/data/nswdata2.html
    """
    dirname = os.path.dirname(__file__)
    abspath = os.path.join(dirname, r"testdata\re78.txt")
    data = pd.read_csv(abspath, index_col=0)
    control = data[data["treat"] == 0].values
    treatment = data[data["treat"] == 1].values
    return control, treatment
    
if __name__ == "__main__":
    control, treatment = load_re78()
    print(control.shape)
    print(treatment.shape)