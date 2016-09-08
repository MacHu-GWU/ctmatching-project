.. image:: https://img.shields.io/pypi/v/ctmatching.svg

.. image:: https://img.shields.io/pypi/l/ctmatching.svg

.. image:: https://img.shields.io/pypi/pyversions/ctmatching.svg


Welcome to ctmatching Documentation
===============================================================================
The `Treatment and control group <https://en.wikipedia.org/wiki/Treatment_and_control_groups>`_ experiment is widely used in comparative experiments. In order to verify that whether a method is significantly working for certain problem, usually we select group of object having same problem, and having similar circumstance. Then we divide them into control and treatment, and perform the method to treatment group.

BUT! Sometimes there's not enough people available that willing to accept the treatment. Usually **treatment group is greatly less than control group**. Then we have to select control group with similar circumstance from public. ``stratified propensity score matching algorithm`` (PSM) is a method for selecting control group. ``ctmatching`` is a python implementation of it.


中文介绍 (Chinese Introduction)
-------------------------------------------------------------------------------
**Propensity score matching (PSM) 倾向评分匹配**

PSM主要用于生物统计中。在生物统计中, 很多实验都要设置 ``对照组/控制组（control group）`` 和 ``实验组（treatment group）``。在一个精心设计的实验中, 对照组和实验组通常在除了实验所导致的结果部分, 都要保证其他情况尽量一致, 这样实验结果才有说服力。

例如我们研究X药品对A疾病的治疗效果, 如果我们选择100个病人, 他们的身体状况都比较相似, 给其中50个人吃药, 另外50个人不吃药。如果过了一个月对照组中的病人有30%身体恶化, 10%的状态不变, 10%的稍许好转。而实验组中的病人有30%都有好转, 那么我们大体上可以说明这个药是有效的。

但是, 在实际的情况下我们通常做不到这一点。因为我们很难找到大量的状态相似的实验对象, 往往我们只能对部分对象做实验, 而去在其他大量没有做实验的对象中, 根据数理统计选择对照组。

同样是X药品和A疾病的例子: 我们在测试A药对B病的治疗效果, 于是我们对50名病病人做实验, 给他们吃了药。接着就需要到社会上找与这50名病人情况类似, 但没有吃药的病人。为了研究X药的有效性, 对于每一个病人我们需要以某种方式在大量人群中, 找到与他们在其他条件相似的对照组。而这种选取对照组的方法, 就叫PSM。


**Quick Links**
-------------------------------------------------------------------------------
- `GitHub Homepage <https://github.com/MacHu-GWU/ctmatching-project>`_
- `Online Documentation <http://pythonhosted.org/ctmatching>`_
- `PyPI download <https://pypi.python.org/pypi/ctmatching>`_
- `Install <install_>`_
- `Issue submit and feature request <https://github.com/MacHu-GWU/ctmatching-project/issues>`_
- `API reference and source code <http://pythonhosted.org/ctmatching/py-modindex.html>`_


.. _install:

Install
-------------------------------------------------------------------------------
``ctmatching`` requires ``numpy >= 1.8.1``, ``scipy >= 0.14.1``, ``pandas >= 0.14.1``, ``scikit-learn >= 0.15.2``.

``ctmatching`` is released on PyPI, so all you need is:

.. code-block:: console

	$ pip install ctmatching

To upgrade to latest version:

.. code-block:: console

	$ pip install --upgrade ctmatching