""" setup.py """

import os
from setuptools import setup, find_packages

NAME = 'eea.indicators'
PATH = NAME.split('.') + ['version.txt']
VERSION = open(os.path.join(*PATH)).read().strip()

setup(
 name=NAME,
 version=VERSION,
 description="EEA Indicators",
 long_description_content_type="text/x-rst",
 long_description=open("README.rst").read() + "\n" +
                  open(os.path.join("docs", "HISTORY.txt")).read(),
 url="https://github.com/eea/eea.indicators",
      # https://pypi.python.org/pypi?%3Aaction=list_classifiers
 classifiers=[
     "Framework :: Zope2",
     "Framework :: Plone",
     "Framework :: Plone :: 4.0",
     "Framework :: Plone :: 4.1",
     "Framework :: Plone :: 4.2",
     "Framework :: Plone :: 4.3",
     "Programming Language :: Zope",
     "Programming Language :: Python",
     "Programming Language :: Python :: 2.7",
     "Topic :: Software Development :: Libraries :: Python Modules",
     "License :: OSI Approved :: GNU General Public License (GPL)",
 ],
 keywords='EEA indicators Add-ons Plone Zope',
 author='European Environment Agency: IDM2 A-Team',
 author_email='eea-edw-a-team-alerts@googlegroups.com',
 license='GPL',
 packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
 namespace_packages=['eea'],
 include_package_data=True,
 zip_safe=False,
 install_requires=[
     "setuptools",
     "Products.ATVocabularyManager",
     "Products.DataGridField",
     "Products.UserAndGroupSelectionWidget",
     "Products.EEAContentTypes",
     "eea.facetednavigation > 10.0",
     "eea.themecentre",
     "eea.dataservice",
     "eea.workflow",
     'eea.relations',
     'zope.traversing',
     "eea.forms",
     'eea.tags',
     'eea.versions > 10.9',
     'eea.app.visualization',
     'Products.CompoundField',
 ],
 entry_points="""
 # -*- Entry points: -*-
 """,
 )
