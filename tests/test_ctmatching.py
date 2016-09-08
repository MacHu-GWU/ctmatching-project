#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import pytest
import numpy as np
from ctmatching.dataset import load_re78
from ctmatching.core import (
    exam_input,
    non_stratified_matching,
    stratified_matching,
    non_repeat_index_matching,
    independent_index_matching,
    psm,
    grouper,
)
from ctmatching.exc import InputError


def test_exam_input():
    control = np.random.random((100, 6))
    treatment = np.random.random((10, 6))

    stratify_order = [[1], [3], [0, 2, 4], [5]]
    exam_input(control, treatment, stratify_order)

    stratify_order = [[0, 1, 2, 3], [2, 3, 4, 5]]
    exam_input(control, treatment, stratify_order)

    with pytest.raises(InputError):
        stratify_order = [[0, 0], [1, 1]]
        exam_input(control, treatment, stratify_order)


def test_non_stratified_matching():
    control = np.random.random((100, 6))
    treatment = np.random.random((10, 6))
    nn_index = non_stratified_matching(control, treatment)


def test_non_repeat_index_matching():
    control = np.random.random((100, 6))
    treatment = np.random.random((10, 6))
    nn_index = non_stratified_matching(control, treatment)
    (
        selected_control_index,
        selected_control_index_for_each_treatment,
    ) = non_repeat_index_matching(nn_index, k=3)
    assert len(selected_control_index) == len(set(selected_control_index))


def test_independent_index_matching():
    control = np.random.random((30, 6))
    treatment = np.random.random((10, 6))
    nn_index = non_stratified_matching(control, treatment)
    (
        selected_control_index,
        selected_control_index_for_each_treatment,
    ) = independent_index_matching(nn_index, k=5)
    assert len(selected_control_index) > len(set(selected_control_index))


def test_psm():
    control, treatment = load_re78()
    use_col = [1, 2, 3, 4, 5, 6]
    stratify_order = [[1], [3], [0, 2, 4], [5]]
    (
        selected_control_index,
        selected_control_index_for_each_treatment,
    ) = psm(control, treatment, use_col, stratify_order, True, 3)

    for treatment_sample, control_samples in grouper(
            control, treatment, selected_control_index_for_each_treatment):

        print("\n--- %s ---" % treatment_sample)
        print("--- match:")
        for control_sample in control_samples:
            print("    %s" % control_sample)


if __name__ == "__main__":
    import os
    pytest.main(["--tb=native", "-s", os.path.basename(__file__)])
