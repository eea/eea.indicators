from Products.PloneTestCase.layer import PloneSite
from eea.indicators.tests.base import BaseIndicatorsTestCase
import Testing
import os, sys


def test_suite():
    from unittest import TestSuite
    from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite

    s1 = ZopeDocFileSuite('overview.txt',
                         package='eea.indicators.doc',
                         test_class=BaseIndicatorsTestCase)
    s1.layer = PloneSite
    return TestSuite((s1,))

