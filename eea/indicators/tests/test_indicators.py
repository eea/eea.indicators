""" Test suites for eea.indicators
"""

import doctest
from unittest import TestSuite

from Products.PloneTestCase.layer import PloneSite
from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite
from eea.indicators.tests.base import BaseIndicatorsTestCase

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)


def test_suite():
    """test suite"""

    s1 = ZopeDocFileSuite('install.txt',
                         package='eea.indicators.doc',
                         test_class=BaseIndicatorsTestCase,
                         #options=OPTIONFLAGS
                         )

    s2 = ZopeDocFileSuite('contenttypes.txt',
                         package='eea.indicators.doc',
                         test_class=BaseIndicatorsTestCase,
                         #options=OPTIONFLAGS
                         )
    s2.layer = PloneSite

    s3 = ZopeDocFileSuite('permissions.txt',
                         package='eea.indicators.doc',
                         test_class=BaseIndicatorsTestCase,
                         #options=OPTIONFLAGS
                         )
    s3.layer = PloneSite

    s4 = ZopeDocFileSuite('marshaller.txt',
                         package='eea.indicators.doc',
                         test_class=BaseIndicatorsTestCase,
                         #options=OPTIONFLAGS
                         )
    s4.layer = PloneSite

    return TestSuite((s1, s2, s3, s4))

