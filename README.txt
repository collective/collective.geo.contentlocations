Introduction
============

collective.geo.contentlocations is a GUI for collective.geo.geographer.

It provides some simple forms to add geographical coordinates to Plone content types.

Requirements
------------
 * plone >= 3.2.1
 * plone.app.z3cform
 * collective.geo.geographer
 * collective.geo.settings
 * Shapely

Installation
============
Before install collective.geo.contentolocations you should install Shapely package and its dependencies (see http://pypi.python.org/pypi/Shapely/ for more informations)

After that just a simple easy_install collective.geo.contentlocations is enough.

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


Contributors
============

* Giorgio Borelli - gborelli
* Silvio Tomatis - silviot
* David Breitkreutz - rockdj
