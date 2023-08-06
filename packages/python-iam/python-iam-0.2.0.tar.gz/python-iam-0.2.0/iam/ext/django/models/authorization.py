import uuid

from django.db import models
from django.contrib.auth.models import Permission


class Authorization(Permission):

    class Meta:
        app_label = 'iam'
        default_permissions = []
        permissions = [
            ('grant', "Grant"),
            ('revoke', "Revoke"),
            ('deny', "Deny")
        ]
        proxy = True
