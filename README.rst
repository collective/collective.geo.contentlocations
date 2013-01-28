Introduction
============

collective.geo.contentlocations is a GUI for `collective.geo.geographer`_.

It provides some simple forms to add geographical coordinates and associated settings to Plone content types.

.. image:: https://secure.travis-ci.org/collective/collective.geo.contentlocations.png
    :target: http://travis-ci.org/collective/collective.geo.contentlocations

Found a bug? Please, use the `issue tracker`_.


.. contents:: Table of contents


Requirements
============

 * `Plone`_ >= 4.0
 * `collective.geo.mapwidget`_
 * `collective.geo.geographer`_


Installation
============
You can install collective.geo.contentlocations as part of a specific project's buildout, by having a buildout configuration such as::

        [buildout]
        ...
        eggs =
            collective.geo.contentlocations
        ...


Contributors
============

* Giorgio Borelli - gborelli
* Silvio Tomatis - silviot
* Gerhard Weis - gweis
* David Beitey - davidjb
* Rob Gietema - robgietema
* Leonardo J. Caballero G - macagua


.. _Plone: http://plone.org
.. _collective.geo.mapwidget: http://pypi.python.org/pypi/collective.geo.mapwidget
.. _collective.geo.geographer: http://pypi.python.org/pypi/collective.geo.geographer
.. _issue tracker: https://github.com/collective/collective.geo.bundle/issues

