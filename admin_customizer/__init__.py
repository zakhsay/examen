from __future__ import absolute_import, unicode_literals

# This makes sure the app is always imported when
# Django starts so that shared tasks work properly
from .celery import app as celery_app
celery = celery_app
__all__ = ('celery_app','celery')
