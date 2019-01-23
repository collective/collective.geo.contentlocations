from setuptools import setup, find_packages
import os

version = '3.3.dev0'

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
          'Products.Archetypes',
          'pygeoif > 0.2',
          'collective.geo.mapwidget >= 2.2',
          'collective.z3cform.mapwidget >= 2.1',
          'collective.geo.geographer >= 2.0',
      ],
      extras_require={
          'test': [
              'plone.app.testing',
              'collective.geo.behaviour',
          ]
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
