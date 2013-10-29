from setuptools import setup, find_packages
import os

version = '3.0'

setup(name='collective.geo.contentlocations',
      version=version,
      description="geo reference for plone contents",
      long_description=open(
          "README.rst").read() + "\n" + open(
              os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
          "Framework :: Plone",
          "Topic :: Internet",
          "Topic :: Scientific/Engineering :: GIS",
          "Programming Language :: Python",
      ],
      keywords='Zope Plone GIS KML Google Maps Bing OpenLayers',
      author='Giorgio Borelli',
      author_email='giorgio@giorgioborelli.it',
      url='https://github.com/collective/collective.geo.contentlocations',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective', 'collective.geo'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFCore',
          'pygeoif > 0.2',
          'collective.geo.mapwidget > 1.6',
          'collective.z3cform.mapwidget > 0.1',
          'collective.geo.geographer > 1.7',
      ],
      extras_require={
          'test': [
              'plone.app.testing',
          ]
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
