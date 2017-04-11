#!/usr/bin/env python

"""
setup.py file for SWIG example
"""

from distutils.core import setup, Extension


example_module = Extension('_DistanceMetricLearner',
                           sources=['_DistanceMetricLearner_wrap.cxx', '_DistanceMetricLearner.cpp'],
                           )

setup (name = '_DistanceMetricLearner',
       version = '0.1',
       author      = "SWIG Docs",
       description = """_DistanceMetricLearner Method""",
       ext_modules = [_DistanceMetricLearner_module],
       py_modules = ["_DistanceMetricLearner"],
       )