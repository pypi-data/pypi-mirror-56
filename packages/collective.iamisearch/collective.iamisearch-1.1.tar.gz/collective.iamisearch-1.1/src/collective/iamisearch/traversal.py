# -*- coding: utf-8 -*-

from ZPublisher.BaseRequest import DefaultPublishTraverse
from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import getUtility

FACETED_VIEWS = ["configure_faceted.html", "@@taxonomy_description"]
IGNORED_NAMES = ["index_html"]


class IAmISearchFolderTraversable(DefaultPublishTraverse):

    taxonomy_id = None

    def publishTraverse(self, request, name):
        """
        """
        if name in self.context.objectIds() or name in FACETED_VIEWS:
            return super(IAmISearchFolderTraversable, self).publishTraverse(
                request, name
            )

        if name in IGNORED_NAMES:
            name = ""
            return super(IAmISearchFolderTraversable, self).publishTraverse(
                request, name
            )

        if request.form.get("taxonomy_term"):
            # Ex: coming from language switcher
            del request.form["taxonomy_term"]
            name = ""
            return super(IAmISearchFolderTraversable, self).publishTraverse(
                request, name
            )

        current_lang = api.portal.get_current_language()[:2]
        normalizer = getUtility(IIDNormalizer)
        taxonomy = getUtility(ITaxonomy, name=self.taxonomy_id)
        data = taxonomy.inverted_data.get(current_lang)
        for key, value in data.items():
            normalized_value = normalizer.normalize(value)
            if normalized_value == name:
                request.form["taxonomy_term"] = name
                name = ""
                return super(IAmISearchFolderTraversable, self).publishTraverse(
                    request, name
                )

        return super(IAmISearchFolderTraversable, self).publishTraverse(request, name)


class IAmFolderTraversable(IAmISearchFolderTraversable):
    """
    """

    taxonomy_id = "collective.taxonomy.iam"


class ISearchFolderTraversable(IAmISearchFolderTraversable):
    """
    """

    taxonomy_id = "collective.taxonomy.isearch"
