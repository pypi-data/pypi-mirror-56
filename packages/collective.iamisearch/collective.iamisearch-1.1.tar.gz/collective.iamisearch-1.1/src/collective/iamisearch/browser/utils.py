# -*- coding: utf-8 -*-

from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from cgi import escape
from collective.iamisearch.interfaces import IIAmFolder
from collective.iamisearch.interfaces import IISearchFolder
from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from plone.api.portal import get_registry_record
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import getMultiAdapter
from zope.component import getUtility


class UtilsView(BrowserView):
    """
    """

    def get_description(self, taxonomy_term=None):
        if not taxonomy_term:
            taxonomy_term = self.request.form.get("taxonomy_term")
        if not taxonomy_term:
            return " "
        current_lang = api.portal.get_current_language()[:2]
        normalizer = getUtility(IIDNormalizer)
        if IIAmFolder.providedBy(self.context):
            taxonomy_id = "collective.taxonomy.iam"
            record_id = "iam_taxonomy_description"
        elif IISearchFolder.providedBy(self.context):
            taxonomy_id = "collective.taxonomy.isearch"
            record_id = "isearch_taxonomy_description"
        else:
            return " "
        taxonomy = getUtility(ITaxonomy, name=taxonomy_id)
        data = taxonomy.inverted_data.get(current_lang)
        for key, value in data.items():
            normalized_value = normalizer.normalize(value)
            if taxonomy_term == key or taxonomy_term == normalized_value:
                mapping = get_registry_record(
                    "{0}.{1}".format(
                        "collective.iamisearch.interfaces.IIamIsearchSettings",
                        record_id,
                    )
                )
                for line in mapping:
                    if key == line["term"] and current_lang == line["lang"]:
                        return line["text"]
        return " "

    def calculate_title(self):
        """
        """
        context_state = getMultiAdapter(
            (self.context, self.request), name=u"plone_context_state"
        )
        page_title = escape(safe_unicode(context_state.object_title()))
        taxonomy_term = self.request.form.get("taxonomy_term")
        if not taxonomy_term:
            return page_title
        current_lang = api.portal.get_current_language()[:2]
        normalizer = getUtility(IIDNormalizer)
        if IIAmFolder.providedBy(self.context):
            taxonomy = getUtility(ITaxonomy, name="collective.taxonomy.iam")
        elif IISearchFolder.providedBy(self.context):
            taxonomy = getUtility(ITaxonomy, name="collective.taxonomy.isearch")
        else:
            return page_title
        data = taxonomy.inverted_data.get(current_lang)
        for key, value in data.items():
            normalized_value = normalizer.normalize(value)
            if normalized_value == taxonomy_term:
                page_title = u"{0} : <span id='taxonomy_term'>{1}</span>".format(
                    page_title, value.lstrip("/")
                )
                break
        return page_title
