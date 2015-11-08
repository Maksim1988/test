__author__ = 'm.senchuk'

import itertools

from nose.loader import TestLoader
from nose import run
from nose.suite import LazySuite

#paths = ("C:\Users\\m.senchuk\\PycharmProjects\\FF4F\\api-tests\\tests\\front_office\\test_search.py:TestSearchSeller",
#        )
#
#
#def run_my_tests():
#    all_tests = ()
#    for path in paths:
#        all_tests = itertools.chain(all_tests, TestLoader().loadTestsFromName(path))
#    suite = LazySuite(all_tests)
#    result = run(suite=suite)
#    assert result is True, "One or more tests FAILED. See console log."
#
#if __name__ == '__main__':
#    run_my_tests()