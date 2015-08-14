#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import os

def load_re78():
    dirname = os.path.dirname(__file__)
    abspath = os.path.join(dirname, r"testdata\re78.txt")
    data = pd.read_csv(abspath, index_col=0)
    control = data[data["treat"] == 0].values
    treatment = data[data["treat"] == 1].values
    return control, treatment
    
if __name__ == "__main__":
    control, treatment = load_re78()
    print(control)
    print(treatment)