import uuid

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser


class Choosable:
    @classmethod
    def choices(cls):
        return [(v.value, v.name) for v in cls]


class BasicQuerySet(models.QuerySet):
    def recently_created(self):
        return self.order_by('-created_at').first()

    def recently_updated(self):
        return self.order_by('-updated_at').first()


class BasicManager(models.Manager.from_queryset(BasicQuerySet)):
    pass


class CreatedAtMixin(models.Model):
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True, editable=False)

    class Meta:
        abstract = True


class UpdatedAtMixin(models.Model):
    updated_at = models.DateTimeField(_('updated_at'), auto_now=True, editable=False)

    class Meta:
        abstract = True


class UUIDPrimaryKeyMixin(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class BasicModelMixin(UUIDPrimaryKeyMixin, CreatedAtMixin, UpdatedAtMixin):
    objects = BasicManager()

    class Meta:
        abstract = True


class BasicModel(BasicModelMixin):
    class Meta:
        abstract = True
