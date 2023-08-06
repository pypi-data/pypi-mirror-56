from django.contrib.sites.models import Site
from django.test import TestCase
import ioc

from iam.domain import Resource
from iam.ext.django.models import ResourceAuthorization
from iam.ext.django.models import Subject
import iam.const


class BasicSubjectPermissionTestCase(TestCase):
    fixtures = ['testusers']

    @ioc.inject('principal', 'iam.PrincipalFactory')
    def setUp(self, principal):
        self.site = Site.objects.get(pk=iam.const.DEFAULT_SITE_ID)
        self.superuser = Subject.objects.get(
            key=iam.const.DEFAULT_SUPERUSER)
        self.user1 = Subject.objects.get(
            key=iam.const.DEFAULT_USER1)
        self.user2 = Subject.objects.get(
            key=iam.const.DEFAULT_USER2)
        ResourceAuthorization.objects.grant(
            self.superuser,
            principal.fromdjangomodel(self.user2),
            'iam.login', Resource.fromdjango(self.site))

    def test_superuser_can_login_site(self):
        is_authorized = self.superuser.has_perm('iam.login', self.site)
        self.assertTrue(self.superuser.is_superuser)
        self.assertTrue(is_authorized)

    def test_user1_can_not_login_site(self):
        is_authorized = self.user1.has_perm('iam.login', self.site)
        self.assertFalse(self.user1.is_superuser)
        self.assertFalse(is_authorized)

    def test_user2_can_login_site(self):
        is_authorized = self.user2.has_perm('iam.login', self.site)
        self.assertFalse(self.user2.is_superuser)
        self.assertTrue(is_authorized)

    @ioc.inject('principal', 'iam.PrincipalFactory')
    def test_user2_can_not_login_site_after_deny_on_site(self, principal):
        is_authorized = self.user2.has_perm('iam.login', self.site)
        self.assertFalse(self.user2.is_superuser)
        self.assertTrue(is_authorized)

        ResourceAuthorization.objects.deny(self.superuser,
            principal.fromdjangomodel(self.user2),
            'iam.login', Resource.fromdjango(self.site))
        if hasattr(self.user2, '_object_perm_cache'):
            delattr(self.user2, '_object_perm_cache')
        is_authorized = self.user2.has_perm('iam.login', self.site)
        self.assertFalse(is_authorized)
