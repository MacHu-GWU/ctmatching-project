Quick Start
================================================================================
``control`` and ``treatment`` is 2d-array like data. Each row is a N-features sample. Let's say ``control`` is Mc x N matrix and ``treatment`` is Mt x N matrix. They don't have to be all numeric data, but we can only use subset of numeric only features for PSM.


Minimal usage
--------------------------------------------------------------------------------
First, import:

We just select most similar sample from control for each treatment sample::

	from __future__ import print_function
	import numpy as np
	from ctmatching import psm, grouper

Create some test data::

	control = np.array([[10., 0., 7.], [1., 4., 8.],])
	treatment = np.array([[8., 3., 8.], [2., -3., 4.],])

Perform psm::

	# by default, use_col = None, stratify_order = None, independent = True, k = 1
	selected_control_index, selected_control_index_for_each_treatment = psm(control, treatment)

Display the matching::

	for treatment_sample, control_samples in grouper(
	    control, treatment, selected_control_index_for_each_treatment):
	    
	    print("\n--- %s ---" % treatment_sample)
	    print("--- match:")
	    for control_sample in control_samples:
	        print("    %s" % control_sample)

The output looks like::

	--- [ 8.  3.  8.] ---
	--- match:
	    [ 10.   0.   7.]

	--- [ 2. -3.  4.] ---
	--- match:
	    [ 1.  4.  8.]


**Want to make feature3 more important? Let's do stratified matching**::


	# use stratified order
	selected_control_index, selected_control_index_for_each_treatment = psm(
	    control, treatment, stratify_order=[[2], [0, 1]])

	for treatment_sample, control_samples in grouper(
	    control, treatment, selected_control_index_for_each_treatment):
	    
	    print("\n--- %s ---" % treatment_sample)
	    print("--- match:")
	    for control_sample in control_samples:
	        print("    %s" % control_sample)

The output looks like::

	--- [ 8.  3.  8.] ---
	--- match:
	    [ 1.  4.  8.]

	--- [ 2. -3.  4.] ---
	--- match:
	    [ 10.   0.   7.]


Advance Usage
--------------------------------------------------------------------------------
In this section, we will use ``ctmatching`` on :mod:`US re78 data <ctmatching.dataset>`. The full description of this data is `here <http://users.nber.org/~rdehejia/data/nswdata2.html>`_

In control, treat group matching, we may have these considers

- Sometime, we only want selected columns for matching. 
- Sometime, we want search Minimal similar sample by feature1, with same feature1 value, then start considering feature2. 
- We may need take multiple attributes into account together. 
- We may want every treatment sample to multiple different control samples.

OK, let's take a look at the hard code::

	from ctmatching import load_re78

	control, treatment = load_re78() # load data

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

The output looks like::

	--- ['NSW1' '1' '37' '11' '1' '0' '1' '1' '0.0' '0.0' '9930.046'] ---
	--- match:
	    ['PSID368' '0' '40' '11' '1' '0' '1' '1' '0.0' '0.0' '0.0']
	    ['PSID375' '0' '46' '11' '1' '0' '1' '1' '0.0' '0.0' '2820.98']

	--- ['NSW2' '1' '22' '9' '0' '1' '0' '1' '0.0' '0.0' '3595.894'] ---
	--- match:
	    ['PSID341' '0' '20' '9' '0' '1' '0' '1' '1500.798' '0.0' '12618.31']
	    ['PSID334' '0' '19' '9' '0' '1' '0' '1' '1822.118' '0.0' '3372.172']

	--- ['NSW3' '1' '30' '12' '1' '0' '0' '0' '0.0' '0.0' '24909.45'] ---
	--- match:
	    ['PSID99' '0' '28' '12' '1' '0' '0' '0' '16722.34' '4253.806' '7314.747']
	    ['PSID159' '0' '28' '12' '1' '0' '0' '0' '6285.328' '2255.806' '7310.313']
	...

Not too hard, right?

If you want to take one more step further, you should check this API reference :func:`ctmatching.core.psm`