from setuptools import setup, find_packages
import os

version = '0.2dev'

setup(name='collective.geo.contentlocations',
      version=version,
      description="geo reference for plone contents",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Giorgio Borelli',
      author_email='giorgio@giorgioborelli.it',
      url='https://svn.plone.org/svn/collective/collective.geo.contentlocations',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.geo'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          #'Shapely',
          'plone.z3cform',
          'collective.geo.openlayers',
          'collective.geo.geographer',
          'collective.geo.settings',
          'collective.geo.geopoint',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
