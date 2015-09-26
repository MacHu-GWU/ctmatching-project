#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
``ctmatching`` algoritm example data set loader.

About re78 data:

- 1978 US people earning data by race, age, gender, educations.
- 429 control samples, 185 treatment samples. Each sample has 10 properties.
  except ID

Full description of this data: http://users.nber.org/~rdehejia/data/nswdata2.html
"""

import numpy as np
import site
import os

def load_re78():
    """re78 data loader
    
    Usage::
    
        >>> from ctmatching import load_re78
        >>> control, treat = load_re78()
        >>> len(control)
        429
        >>> len(treat)
        185
    """
    abspath = os.path.join(
        site.getsitepackages()[1], "ctmatching", "testdata", "re78.txt")    

    with open(abspath, "rb") as f:
        lines = f.read().decode("utf-8").split("\n")
        
    columns = lines[0].strip().split(",")

    control = list()
    treat = list()

    for line in lines[1:]:
        record = line.strip().split(",")

        for i in [1, 2, 3, 4, 5, 6, 7]:
            record[i] = int(record[i])
        for i in [8, 9, 10]:
            record[i] = float(record[i])
        
        if record[1]:
            treat.append(record)
        else:
            control.append(record)
    
    return np.array(control), np.array(treat)
    
if __name__ == "__main__":
    control, treat = load_re78()