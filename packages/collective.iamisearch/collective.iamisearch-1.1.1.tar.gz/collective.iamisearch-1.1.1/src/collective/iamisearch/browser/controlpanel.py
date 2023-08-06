# -*- coding: utf-8 -*-

from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from z3c.form import form

from collective.iamisearch import _
from collective.iamisearch.interfaces import IIamIsearchSettings


class IamIsearchSettingsEditForm(RegistryEditForm):

    form.extends(RegistryEditForm)
    schema = IIamIsearchSettings
    label = _(u"I am / I search settings")

    def updateFields(self):
        super(IamIsearchSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(IamIsearchSettingsEditForm, self).updateWidgets()


SettingsView = layout.wrap_form(IamIsearchSettingsEditForm, ControlPanelFormWrapper)
