from django.db import models as django_models

from waldur_core.core import managers as core_managers


class OfferingManager(core_managers.GenericKeyMixin, django_models.Manager):
    pass


class OrderItemManager(core_managers.GenericKeyMixin, django_models.Manager):
    pass
