from ftw.labels.config import COLORS
from ftw.labels.interfaces import ILabelJarChild
from ftw.labels.interfaces import ILabelJar
from ftw.labels.interfaces import ILabelRoot
from ftw.labels.portlets.assignments import LabelJarAssignment
from ftw.labels.utils import title_by_user
from plone.app.portlets.portlets.base import NullAddForm
from plone.app.portlets.portlets.base import Renderer
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class AddForm(NullAddForm):

    def create(self):
        return LabelJarAssignment()


class Renderer(Renderer):
    render = ViewPageTemplateFile('labeljar.pt')

    @property
    def available(self):
        if 'portal_factory' in self.context.absolute_url():
            return False
        if ILabelJarChild.providedBy(self.context):
            if not self.label_root_obj:
                return False
        elif not ILabelRoot.providedBy(self.context):
            return False
        if not self.can_edit and not self.labels:
            return False
        return True

    @property
    def labels(self):
        return ILabelJar(self.label_root_obj).list()

    @property
    def colors(self):
        return COLORS

    @property
    def can_edit(self):
        mtool = getToolByName(self.context, 'portal_membership')
        return mtool.checkPermission(
            'ftw.labels: Manage Labels Jar', self.context)

    @property
    def label_root_obj(self):
        try:
            return ILabelJar(self.context)
        except LookupError:
            return None

    def label_title(self, title, by_user):
        return title_by_user(title, by_user)
