from setuptools import setup, find_packages
import os

name = 'eea.indicators'
path = name.split('.') + ['version.txt']
version = open(os.path.join(*path)).read().strip()

setup(name='eea.indicators',
      version=version,
      description="EEA Indicators site",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='EEA indicators',
      author='Tiberiu Ichim, Eau de Web',
      author_email='tiberiu@eaudeweb.ro',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      namespace_packages=['eea'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "setuptools",
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )

