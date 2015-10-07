Introduction
================================================================================

The `Treatment and control group <https://en.wikipedia.org/wiki/Treatment_and_control_groups>`_ experiment is widely used in comparative experiments. For a big group of people having similar circumstance, if treatments are applied and we see it works, Bingo, we got what we want to prove now. Knock Knock! Welcome back to reality. In real worlds, **it is usually very difficult to find large amount of people having similar circumstance**. So what we do is only apply treatments to small amount of people, and then select similar people from public. Then we can start comparison.

This, is control treatment matching.

ctmatching is a ``stratified propensity score matching algorithm`` python implementation built on `numpy <http://www.numpy.org/>`_, `pandas <http://pandas.pydata.org/>`_, `sklearn <http://scikit-learn.org/stable/>`_. Thanks for standing on the shoulders of these giants.

For more information about Installation, Usage, API and full documentation:

- `Download, Installation <https://pypi.python.org/pypi/ctmatching>`_
- `Source code <https://github.com/MacHu-GWU/ctmatching-project>`_
- `Documentation <http://www.wbh-doc.com.s3.amazonaws.com/ctmatching/index.html>`_
- `About author <http://ctmatching-project.readthedocs.org/about.html>`_
- `Bug and Issue <https://github.com/MacHu-GWU/ctmatching-project/issues>`_

Download and Install
--------------------------------------------------------------------------------

``ctmatching`` requires ``numpy >= 1.8.1``, ``scipy >= 0.14.1``, ``pandas >= 0.14.1``, ``scikit-learn >= 0.15.2``.

``ctmatching`` is released on PyPI, so all you need is:

.. code-block:: console

	$ pip install ctmatching

To upgrade to latest version:

.. code-block:: console
	
	$ pip install --upgrade ctmatching

If you want to build the source by your self, `download the source code <https://github.com/MacHu-GWU/ctmatching-project/archive/master.zip>`_ and:

.. code-block:: console
	
	$ cd ctmatching-project
	$ python setup.py build
	$ python setup.py install


中文介绍(Chinese Introduction)
================================================================================

**Propensity score matching (PSM) 倾向评分匹配**

PSM主要用于生物统计中。在生物统计中, 很多实验都要设置``对照组/控制组（control group）``和``实验组（treatment group）``。在一个精心设计的实验中, 对照组和实验组通常在除了实验所导致的结果部分, 都要保证其他情况尽量一致, 这样实验结果才有说服力。

例如我们研究X药品对A疾病的治疗效果, 如果我们选择100个病人, 他们的身体状况都比较相似, 给其中50个人吃药, 另外50个人不吃药。如果过了一个月对照组中的病人有30%身体恶化, 10%的状态不变, 10%的稍许好转。而实验组中的病人有30%都有好转, 那么我们大体上可以说明这个药是有效的。

但是, 在实际的实验中我们通常做不到这一点。因为我们很难找到大量的状态相似的实验对象。同样是X药品和A疾病的例子：

我们在测试A药对B病的治疗效果, 于是我们对50名病病人做实验, 给他们吃了药。接着就需要到社会上找与这50名病人情况类似, 但没有吃药的病人。为了研究X药的有效性, 对于每一个病人我们需要以某种方式在社会中找到他们的对照组。而这种匹配的方法, 就叫PSM。