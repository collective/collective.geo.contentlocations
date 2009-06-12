Introduction
============

GUI for zgeo.plone.geographer, provide a simples forms for add coordinates to Plone content types

Requirements
------------
 * plone >= 3.2.1
 * plone.app.z3cform
 * zgeo.plone.geographer
 * collective.geo.settings

Installation
============
Just a simple easy_install collective.geo.contentlocations is enough.

Alternatively, buildout users can install collective.geo.contentlocations as part of a specific project's buildout, by having a buildout configuration such as: ::

        [buildout]
        ...
        eggs = 
            zope.i18n>=3.4
            collective.geo.contentlocations
        ...
        [instance]
        ...
        zcml = 
            collective.geo.contentlocations

Usage
=====
Install this product from the Plone control panel.

After that you have installed the product with quickinstaller tool yoo can go to a Document content type.

You can see the new tab 'Coordinates', click on this tab for insert coordinates to your page.

The form for insert coordinates is a two steps form;

The firts step you can choice the type of coordinates to input

* Point
* Linestring
* Polygon

when you choice Point and click 'Set' button you go to another form.

In the second step you should insert the latitude and the longitude for the point that you want.
You can choice a point coordinates by clicking on the map that appear in the screen.

When you choice a types of coordinates as "LineString" or "Polygon" you should upload a csv file that contains a coordinates series.

The csv file must contains two columns with latitute data in the first column and longitude coordinates in the second one.

