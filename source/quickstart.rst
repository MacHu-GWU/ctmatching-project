Quick Start
================================================================================

Minimal usage
--------------------------------------------------------------------------------

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

The output looks like:

.. code-block:: python

	[ 8.  3.  8.] matches [[ 10.   0.   7.]]
	[ 2. -3.  4.] matches [[ 1.  4.  8.]]

Want to set feature3 more important? Let's do stratified matching:

.. code-block:: python

	selected_control, selected_control_each_treatment = psm(
	    control, treatment, stratify_order=[[2], [0, 1]])

	for treatment_sample, index in zip(treatment, 
		selected_control_each_treatment):
	    print("%s matches %s" % (treatment_sample, control[index]))

The output looks like:

.. code-block:: python

	[ 8.  3.  8.] matches [[ 1.  4.  8.]]
	[ 2. -3.  4.] matches [[ 10.   0.   7.]]


Advance Usage
--------------------------------------------------------------------------------

In this section, we will use ``ctmatching`` on :mod:`US re78 data <ctmatching.dataset>`. The full description of this data is `here <http://users.nber.org/~rdehejia/data/nswdata2.html>`_

In control, treat group matching, we may have these considers

- Sometime, we only want selected columns for matching. 
- Sometime, we want search Minimal similar sample by feature1, with same feature1 value, then start considering feature2. 
- We may need take multiple attributes into account together. 
- We may want every treatment sample to multiple different control samples.

OK, let's take a look at the hard code

.. code-block :: python
	
	from __future__ import print_function
	from ctmatching import psm, load_re78

	control, treatment = load_re78() # load data

	# we only use second, third, ... , 7th column and use 
	# third column (second of use_col) as the dominate feature, 
	# then 5th column as second dominate
	selected_control, selected_control_each_treatment = psm(
	    control, treatment, 
	    use_col=[2,3,4,5,6,7], 
	    stratify_order=[[1],[3],[0,2,4],[5]], 
	    independent=False, k=2)
	    
	for treatment_sample, index in zip(treatment, 
		selected_control_each_treatment):
	    print("=======================================")
	    print(treatment_sample)
	    print("matches")
	    for sample in control[index]:
	        print(sample)

The output looks like:

.. code-block:: python

	=======================================
	[1.0, 37.0, 11.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 9930.046] <=== treatment
	matches
	[0.0, 40.0, 11.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0] <=== matched control1
	[0.0, 46.0, 11.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 2820.98] <=== matched control2
	=======================================
	[1.0, 22.0, 9.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 3595.8940000000002] <=== treatment
	matches
	[0.0, 20.0, 9.0, 0.0, 1.0, 0.0, 1.0, 1500.7979999999998, 0.0, 12618.31] <=== matched control1
	[0.0, 19.0, 9.0, 0.0, 1.0, 0.0, 1.0, 1822.118, 0.0, 3372.172] <=== matched control2

Not too hard, right?

If you want to take one more step further, you can check this API reference :func:`ctmatching.core.psm`