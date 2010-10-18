from Products.PloneTestCase.layer import PloneSite
from eea.indicators.tests.base import BaseIndicatorsTestCase
import Testing
import os, sys


def test_suite():
    from unittest import TestSuite
    from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite

    s1 = ZopeDocFileSuite('install.txt',
                         package='eea.indicators.doc',
                         test_class=BaseIndicatorsTestCase)

    s2 = ZopeDocFileSuite('contenttypes.txt',
                         package='eea.indicators.doc',
                         test_class=BaseIndicatorsTestCase)
    s2.layer = PloneSite

    s3 = ZopeDocFileSuite('permissions.txt',
                         package='eea.indicators.doc',
                         test_class=BaseIndicatorsTestCase)
    s3.layer = PloneSite
    return TestSuite((s1, s2, s3))

