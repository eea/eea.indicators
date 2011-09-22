""" setup.py """

from setuptools import setup, find_packages
import os

NAME = 'eea.indicators'
PATH = NAME.split('.') + ['version.txt']
VERSION = open(os.path.join(*PATH)).read().strip()

setup(
 name=NAME,
 version=VERSION,
 description="EEA Indicators",
 long_description=open("README.txt").read() + "\n" +
                  open(os.path.join("docs", "HISTORY.txt")).read(),
 url="https://svn.eionet.europa.eu/projects/"
     "Zope/browser/trunk/eea.indicators",
 classifiers=[
     "Framework :: Plone",
     "Programming Language :: Python",
     "Topic :: Software Development :: Libraries :: Python Modules",
   ],
 keywords='EEA indicators ims indicatorsmanagementsystem',
 author=('Alec Ghica (Eaudeweb), Tiberiu Ichim (Eaudeweb), '
         'Antonio De Marinis (EEA), European Environment Agency'),
 author_email='webadmin@eea.europa.eu',
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
     "eea.facetednavigation",
     "eea.themecentre",
     "eea.dataservice",
     "eea.workflow",
     'eea.relations',
     "Products.kupu",
     'zope.traversing',
     "eea.forms"
 ],
 entry_points="""
 # -*- Entry points: -*-
 """,
 )

