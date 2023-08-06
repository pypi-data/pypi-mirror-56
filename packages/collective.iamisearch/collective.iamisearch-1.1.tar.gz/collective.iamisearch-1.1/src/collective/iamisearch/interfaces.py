# -*- coding: utf-8 -*-

from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from plone.autoform.directives import widget
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from collective.iamisearch import _


class IIamTaxonomyTermSchema(Interface):

    lang = schema.Choice(
        title=_(u"Language"),
        vocabulary="plone.app.vocabularies.SupportedContentLanguages",
        required=True,
    )

    term = schema.Choice(
        title=_(u"I am Term"), vocabulary="collective.taxonomy.iam", required=True
    )

    text = schema.Text(title=_(u"Description"), required=True)


class ISearchTaxonomyTermSchema(Interface):

    lang = schema.Choice(
        title=_(u"Language"),
        vocabulary="plone.app.vocabularies.SupportedContentLanguages",
        required=True,
    )

    term = schema.Choice(
        title=_(u"I search Term"),
        vocabulary="collective.taxonomy.isearch",
        required=True,
    )

    text = schema.Text(title=_(u"Description"), required=True)


class IIamIsearchSettings(Interface):
    """"""

    iam_taxonomy_description = schema.List(
        title=_(u"Descriptions to show above I am faceted search"),
        required=False,
        value_type=DictRow(title=_(u"Value"), schema=IIamTaxonomyTermSchema),
    )
    widget(iam_taxonomy_description=DataGridFieldFactory)

    isearch_taxonomy_description = schema.List(
        title=_(u"Descriptions to show above I search faceted search"),
        required=False,
        value_type=DictRow(title=_(u"Value"), schema=ISearchTaxonomyTermSchema),
    )
    widget(isearch_taxonomy_description=DataGridFieldFactory)


class ICollectiveIamisearchLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IIAmFolder(Interface):
    """Marker interface for I Am folder(s)."""


class IISearchFolder(Interface):
    """Marker interface for I Search folder(s)."""
