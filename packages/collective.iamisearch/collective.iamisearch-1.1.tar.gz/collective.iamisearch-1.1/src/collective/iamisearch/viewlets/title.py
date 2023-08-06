# -*- coding: utf-8 -*-

from Products.CMFPlone.utils import safe_unicode
from cgi import escape
from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from plone.app.layout.viewlets.common import TitleViewlet
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import getMultiAdapter
from zope.component import getUtility


class IamISearchTitleViewlet(TitleViewlet):

    taxonomy_id = None

    @property
    def page_title(self):
        """ Add chosen taxonomy value in page title (for SEO)
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
        taxonomy = getUtility(ITaxonomy, name=self.taxonomy_id)
        data = taxonomy.inverted_data.get(current_lang)
        for key, value in data.items():
            normalized_value = normalizer.normalize(value)
            if normalized_value == taxonomy_term:
                page_title = u"{0} : {1}".format(page_title, value.lstrip("/"))
                break
        return escape(safe_unicode(page_title))


class IAmTitleViewlet(IamISearchTitleViewlet):

    taxonomy_id = "collective.taxonomy.iam"


class ISearchTitleViewlet(IamISearchTitleViewlet):

    taxonomy_id = "collective.taxonomy.isearch"
