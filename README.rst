Welcome to control treatment matching algorithm's documentation!
================================================================

Documentation: `click here. <http://ctmatching.readthedocs.org/>`_

Introduction
------------

`Treatment and control group <https://en.wikipedia.org/wiki/Treatment_and_control_groups>`_ experiment is widely used in comparative experiments. For a big group of people having similar circumstance, if treatments are applied and we see it works, Bingo, we got what we want to prove now. Knock Knock! Welcome back to reality. In real worlds, **it is usually very difficult to find large amount of people having similar circumstance**. So what we do is only apply treatments to small amount of people, and then select similar people from public. Then we can start comparison.

This, is control treatment matching.

ctmatching is a ``stratified propensity score matching algorithm`` python implementation built on `numpy <http://www.numpy.org/>`_, `pandas <http://pandas.pydata.org/>`_, `sklearn <http://scikit-learn.org/stable/>`_. Thanks for standing on the shoulders of these giants.


ctmatching Installation
=======================
This part of the documentation covers the installation of ctmatching. The first step to using any software package is getting it properly installed.


Development Version
-------------------
Follow my `github repository <https://github.com/MacHu-GWU/ctmatching>`_ is always the best way to get lastest version.


Installation for Dummies
------------------------

Install windtalker in windows is easy.

First, go to `github repository <https://github.com/MacHu-GWU/ctmatching>`_ and download the zip.

Second, open command line console:

.. code-block :: bat

	cd ctmatching\src\ctmatching
	python zzz_manual_install.py

the script can automatically find installed Python and install windtalker to it's site-packages


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


License
=======

ctmatching is an open source project by Sanhe Hu.

Copyright (c) 2015 Sanhe Hu.

The MIT License (MIT)

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED “AS IS” AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

Chinese Quick Doc[中文快速文档]
===============================

**Propensity score matching (PSM) 倾向评分匹配**

PSM主要用于生物统计中。在生物统计中, 很多实验都要设置"对照组/控制组（control group）"和"实验组（treatment group）"。在一个精心设计的实验中, 对照组和实验组通常在除了实验所导致的结果部分, 都要保证其他情况尽量一致, 这样实验结果才有说服力。

例如我们研究X药品对A疾病的治疗效果, 如果我们选择100个病人, 他们的身体状况都比较相似, 给其中50个人吃药, 另外50个人不吃药。如果过了一个月对照组中的病人有30%身体恶化, 10%的状态不变, 10%的稍许好转。而实验组中的病人有30%都有好转, 那么我们大体上可以说明这个药是有效的。

但是, 在实际的实验中我们通常做不到这一点。因为我们很难找到大量的状态相似的实验对象。同样是X药品和A疾病的例子：

我们在测试A药对B病的治疗效果, 于是我们对50名病病人做实验, 给他们吃了药。接着就需要到社会上找与这50名病人情况类似, 但没有吃药的病人。为了研究X药的有效性, 对于每一个病人我们需要以某种方式在社会中找到他们的对照组。而这种匹配的方法, 就叫PSM。