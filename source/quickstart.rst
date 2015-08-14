Quick Start
===========

Minimal usage
-------------

We just select most similar sample from control for each treatment sample:

.. code-block :: python

	from __future__ import print_function
	from ctmatching import psm
	import numpy as np

	control = np.array([[10., 0., 7.], [1., 4., 8.],])
	treatment = np.array([[8., 3., 8.], [2., -3., 4.],])

	# by default, use_col = None, stratify_order = None, 
	# independent = True, k = 1
	selected_control, selected_control_each_treatment = psm(
	    control, treatment)

	for treatment_sample, index in zip(treatment, 
		selected_control_each_treatment):
	    print("%s matches %s" % (treatment_sample, control[index]))

	>>> [ 8.  3.  8.] matches [[ 10.   0.   7.]]
	>>> [ 2. -3.  4.] matches [[ 1.  4.  8.]]

Want to set feature3 more important? Let's do stratified matching:

.. code-block :: python

	selected_control, selected_control_each_treatment = psm(
	    control, treatment, stratify_order=[[2], [0, 1]])

	for treatment_sample, index in zip(treatment, 
		selected_control_each_treatment):
	    print("%s matches %s" % (treatment_sample, control[index]))

	>>> [ 8.  3.  8.] matches [[ 1.  4.  8.]]
	>>> [ 2. -3.  4.] matches [[ 10.   0.   7.]]


Advance Usage
-------------

Sometimes we only want selected columns to use for matching. Sometimes we want search Minimal similar sample by feature1, with same feature1 value, then start considering feature2. We may need multiple matches. We may want every treatment sample to select different control samples.

For description of all arguments, go here `Arguments`_.

A complicate example looks like: 

.. code-block :: python
	
	from __future__ import print_function
	from ctmatching import psm, load_re78

	control, treatment = load_re78()

	# we only use second, third, ... , 7th column and use 
	# third column (second of use_col) as the dominate feature, 
	# then 5th column as second dominate
	selected_control, selected_control_each_treatment = psm(
	    control, treatment, 
	    use_col=[1,2,3,4,5,6], 
	    stratify_order=[[1],[3],[0,2,4],[5]], 
	    independent=False, k=2)
	    
	for treatment_sample, index in zip(treatment, 
		selected_control_each_treatment):
	    print("=======================================")
	    print(treatment_sample.tolist())
	    print("matches")
	    for sample in control[index].tolist():
	        print(sample)

	>>> =======================================
	>>> [1.0, 37.0, 11.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 9930.046]
	>>> matches
	>>> [0.0, 40.0, 11.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0]
	>>> [0.0, 46.0, 11.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 2820.98]
	>>> =======================================
	>>> [1.0, 22.0, 9.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 3595.8940000000002]
	>>> matches
	>>> [0.0, 20.0, 9.0, 0.0, 1.0, 0.0, 1.0, 1500.7979999999998, 0.0, 12618.31]
	>>> [0.0, 19.0, 9.0, 0.0, 1.0, 0.0, 1.0, 1822.118, 0.0, 3372.172]

Not too hard, right?

Arguments
~~~~~~~~~

**control**: control group sample data, m1 x n matrix, #m1 samples, n dimension vector

example: ::

	[[c1_1, c1_2, ..., c1_n],
	 [c2_1, c2_2, ..., c2_n],
	 ...,
	 [cm1_1, cm1_2, ..., cm1_n],]
         

**treatment**: control group sample data, m2 x n matrix, #m2 samples, n dimension vector

example: similar to control


**use_col**: list of column index, default None (use all)

example: ::

    [0, 1, 4, 6, 7, 9] -> use first, second, fifth, ... columns


**stratify_order**: list of list, default None (use normal nearest neighbor)

example: ::

    for input data has 6 columns
    [[0], [1, 2, 3], [4], [5]] -> first feature has highest priority, [second, third,
    forth] features' has second highest priority by mean of euclidean distance, ... 


**k**: int, default 1. number of samples selected from control group


Returns
~~~~~~~

**selected_control_index**: selected control sample index

example (k=3): ::

    m2*k-length array: [7, 120, 43, 54, 12, 98, ..., 71, 37, 14]


**selected_control_index_for_each_treatment**: selected control sample index for each treatment sample
   
example (k=3): ::

    [[7, 120, 43],
     [54, 12, 98],
     ...,
     [71, 37, 14],] -> for treatment[0], we have control[7], control[120], control[43]
     matched by mean of stratification.