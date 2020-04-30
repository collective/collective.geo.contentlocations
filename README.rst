Introduction
============

collective.geo.contentlocations is a GUI for `collective.geo.geographer`_.

It provides some simple forms to add geographical coordinates and associated settings to Plone content types.

.. contents:: Table of contents


Requirements
============

 * `Plone`_ >= 4.0
 * `collective.geo.mapwidget`_
 * `collective.geo.geographer`_


Documentation
=============

Full documentation for end users can be found in the "docs" folder.
It is also available online at https://collectivegeo.readthedocs.io/


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


Tests status
============

This add-on is tested using Travis CI. The current status of the add-on is:

.. image:: https://img.shields.io/travis/collective/collective.geo.contentlocations/master.svg
    :target: https://travis-ci.org/collective/collective.geo.contentlocations

.. image:: http://img.shields.io/pypi/v/collective.geo.contentlocations.svg
   :target: https://pypi.org/project/collective.geo.contentlocations


Contribute
==========

Have an idea? Found a bug? Let us know by `opening a ticket`_.

- Issue Tracker: https://github.com/collective/collective.geo.contentlocations/issues
- Source Code: https://github.com/collective/collective.geo.contentlocations
- Documentation: https://collectivegeo.readthedocs.io/


Contributors
============

* Giorgio Borelli - gborelli
* Silvio Tomatis - silviot
* Gerhard Weis - gweis
* David Beitey - davidjb
* Rob Gietema - robgietema
* Leonardo J. Caballero G. - macagua


License
=======

The project is licensed under the GPL.


.. _Plone: https://plone.org/
.. _collective.geo.mapwidget: https://pypi.org/project/collective.geo.mapwidget
.. _collective.geo.geographer: https://pypi.org/project/collective.geo.geographer
.. _`opening a ticket`: https://github.com/collective/collective.geo.bundle/issues
.. _documentation: https://docs.plone.org/manage/installing/installing_addons.html
