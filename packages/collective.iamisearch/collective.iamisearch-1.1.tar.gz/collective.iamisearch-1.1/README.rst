=====================
collective.iamisearch
=====================

.. image:: https://travis-ci.com/affinitic/collective.iamisearch.svg?branch=master
    :target: https://travis-ci.com/affinitic/collective.iamisearch


This products allows you to categorize contents with terms from two editable taxonomies and get a dropdown menu with those terms to find related contents.
There are :

- "I am" terms
- "I search" terms


Features
--------

- Adds a viewlet with dropdown menus ("I am" & "I search")
- Each terms in menus points to faceted results for this term
- SEO optimized (page URL, page title, page H1)
- Allows to display custom descriptions above faceted searches, configured by
  value & language through a configlet


Translations
------------

This product has been translated into

- French
- Dutch


Installation
------------

Install collective.iamisearch by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.iamisearch


and then running ``bin/buildout``


TODO
----

- Make folder search / url calculation more robust (by using it's interface)
- Don't translate Faceted in XML but in code


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.iamisearch/issues
- Source Code: https://github.com/collective/collective.iamisearch


License
-------

The project is licensed under the GPLv2.


Credits
-------

This package was developed by `Affinitic team <https://github.com/affinitic>`_.

.. image:: http://www.affinitic.be/affinitic_logo.png
   :alt: Affinitic website
   :target: http://www.affinitic.be

``collective.iamisearch`` is licensed under GNU General Public License, version 2.
