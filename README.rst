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


Translations
============

This product has been translated into

- Danish.

- German.

- Spanish.

- French.

- Italian.

- Dutch.

- Brazil Portuguese.

- Chinese Simplified.

- Traditional Chinese.

You can contribute for any message missing or other new languages, join us at 
`Plone Collective Team <https://www.transifex.com/plone/plone-collective/>`_ 
into *Transifex.net* service with all world Plone translators community.


Installation
============

This addon can be installed has any other addons, please follow official
documentation_.


Upgrading
=========

Version 3.0
-----------

If you are upgrading from an older version to 3.0, you may need to run
upgrade steps. To do this, follow these steps:

#. Browse to ``portal_setup`` in the ZMI of your site
#. Click onto the ``Upgrades`` tab
#. Select ``collective.geo.contentlocations:default`` from the drop-down list and
   click ``Choose Profile``
#. Observe any available upgrades and click the ``Upgrade`` button if any
   are present.


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
.. _documentation: http://plone.org/documentation/kb/installing-add-ons-quick-how-to
