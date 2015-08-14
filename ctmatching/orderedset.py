#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module description
~~~~~~~~~~~~~~~~~~

This module provide a pure python OrderedSet data type implementation.
inspired by http://code.activestate.com/recipes/576694/

Ordered set is a set that remembers original insertion order. Also support
add item, remove item, iterate, union, intersect, difference, classic set
operations.

Note: this is not a high performance implementation, don't use this for 
big data and product environment. But there's are better one:

orderedset: a Cython implementation. https://pypi.python.org/pypi/orderedset


Usage examples
~~~~~~~~~~~~~~

Add, discard, pop::

    >>> s = OrderedSet()
    >>> s.add(1)
    >>> s.add(2)
    >>> s.add(3)
    >>> s
    OrderedSet([1, 2, 3])
    
    >>> s.discard(2)
    >>> s
    OrderedSet([1, 3])
    
    >>> s.pop()
    3
    >>> s
    OrderedSet([1])
    
Union, intersect, difference::

    >>> s = OrderedSet("abracadaba") # {"a", "b", "r", "c", "d"}
    >>> t = OrderedSet("simcsalabim") # {"s", "i", "m", "c", "a", "l", "b"}
    >>> s | t # s union t
    OrderedSet(['a', 'b', 'r', 'c', 'd', 's', 'i', 'm', 'l'])
    
    >>> s & t # s intersect t
    OrderedSet(['c', 'a', 'b'])
    
    >>> s - t # s different t
    OrderedSet(['r', 'd'])

About
~~~~~

**Compatibility**

- Python2: Yes
- Python3: Yes
    

**Prerequisites**

- None

class, method, func, exception
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from __future__ import print_function
import collections

class OrderedSet(collections.MutableSet):
    """A light weight OrderedSet data type pure Python implementation.
    """
    def __init__(self, iterable=None):
        self.end = end = [] 
        end += [None, end, end] # sentinel node for doubly linked list
        self.map = {}           # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        """Add an item to the OrderedSet.
        
        Usage::
        
            >>> s = OrderedSet()
            >>> s.add(1)
            >>> s.add(2)
            >>> s.add(3)
            >>> s
            OrderedSet([1, 2, 3])
            
        **中文文档**
        
        添加一个元素, 如果该元素已经存在, 则不会有任何作用。
        """
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        """Remove a item from its member if it is a member.

        Usage::
        
            >>> s = OrderedSet([1, 2, 3])
            >>> s.discard(2)
            >>> s
            OrderedSet([1, 3])
            
        **中文文档**
        
        从有序集合中删除一个元素, 同时保持集合依然有序。
        """
        if key in self.map:        
            key, prev, next_item = self.map.pop(key)
            prev[2] = next_item
            next_item[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        """Remove and returns the last added item.
    
        Usage::
        
            >>> s = OrderedSet([1, 2, 3])
            >>> s.pop()
            3
            >>> s
            OrderedSet([1, 2])
            
        **中文文档**
        
        移除并返回最后添加的元素。
        """
        if not self:
            raise KeyError("set is empty")
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return "%s()" % (self.__class__.__name__,)
        return "%s(%r)" % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)

    @staticmethod
    def union(*argv):
        """Returns union of sets as a new set. basically it's
        Items are ordered by set1, set2, ...
        
        **中文文档**
        
        求多个有序集合的并集, 按照第一个集合, 第二个, ..., 这样的顺序。
        """
        res = OrderedSet()
        for ods in argv:
            res = res | ods
        return res
    
    @staticmethod
    def intersection(*argv):
        """Returns the intersection of multiple sets.
        Items are ordered by set1, set2, ...

        **中文文档**
        
        求多个有序集合的交集, 按照第一个集合, 第二个, ..., 这样的顺序。
        """
        res = OrderedSet(argv[0])
        for ods in argv:
            res = ods & res
        return res

############
# Unittest #
############

if __name__ == "__main__":
    import unittest

    class OrderedSetUnittest(unittest.TestCase):
        def test_add_pop_and_discard(self):
            """test, add(item), pop(last=True/False), discard(item) method
            """
            s = OrderedSet("abcde")
            self.assertListEqual(list(s), ["a", "b", "c", "d", "e"])
            s.pop()
            self.assertListEqual(list(s), ["a", "b", "c", "d"])
            s.pop(last=False)
            self.assertListEqual(list(s), ["b", "c", "d"])
            s.discard("c")
            self.assertListEqual(list(s), ["b", "d"])
        
        def test_union_intersect_and_difference(self):
            """test union, intersect, difference operation
            """
            s = OrderedSet("abracadaba") # {"a", "b", "r", "c", "d"}
            t = OrderedSet("simcsalabim") # {"s", "i", "m", "c", "a", "l", "b"}
            
            self.assertListEqual(list(s | t), # s union t
                ["a", "b", "r", "c", "d", "s", "i", "m", "l"])
            
            self.assertListEqual(list(s & t), # s intersect t
                ["c", "a", "b"])
            
            self.assertListEqual(list(s - t), # s different t
                ["r", "d"])
        
        def test_staticmethod(self):
            """test customized batch union and intersect static method
            """
            r = OrderedSet("buag") # {"b", "u", "a", "g"}
            s = OrderedSet("abracadaba") # {"a", "b", "r", "c", "d"}
            t = OrderedSet("simcsalabim") # {"s", "i", "m", "c", "a", "l", "b"}
            
            # r union s union t
            self.assertListEqual(list(OrderedSet.union(r, s, t)), 
                ["b", "u", "a", "g", "r", "c", "d", "s", "i", "m", "l"])
            
            # r intsect s and t
            self.assertListEqual(list(OrderedSet.intersection(r, s, t)),
                ["b", "a"])
            
    unittest.main()