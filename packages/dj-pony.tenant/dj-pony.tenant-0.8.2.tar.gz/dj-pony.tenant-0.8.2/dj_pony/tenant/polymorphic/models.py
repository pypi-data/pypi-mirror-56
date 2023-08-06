from django.db import models
from polymorphic.managers import PolymorphicManager
from polymorphic.models import PolymorphicModel
from dj_pony.tenant.settings import get_setting
from dj_pony.tenant.polymorphic.managers import PolymorphicSingleTenantModelManager, PolymorphicMultipleTenantModelManager
from dj_pony.tenant.helpers import get_current_tenant
from dj_pony.tenant.exceptions import TenantNotFoundError


def default_tenant_function():
    current_tenant = get_current_tenant()
    if current_tenant is not None:
        return current_tenant.pk
    from dj_pony.tenant.models import Tenant
    default_tenant = Tenant.objects.filter(slug=get_setting("DEFAULT_TENANT_SLUG")).first()
    return default_tenant.pk


# TODO: This is a fragile abstract base model and should be refactored to be a proper mixin!
#  While its good enough for now, it does require undocumented knowledge.
class PolymorphicSingleTenantModelMixin(PolymorphicModel):
    """
    Instances of models inheriting from this mixin are associated with one tenant.

    One Tenant -> Many instances of a Model

    Example:
        Tenant 1 - Instance 1
        Tenant 1 - Instance 2
        Tenant 2 - Instance 3
        Tenant 1 - Instance 4
        Tenant 2 - Instance 5
    """

    tenant = models.ForeignKey(
        "tenant.Tenant", default=default_tenant_function, on_delete=models.CASCADE
    )

    objects = PolymorphicSingleTenantModelManager()

    original_manager = PolymorphicManager()
    tenant_objects = PolymorphicSingleTenantModelManager()

    class Meta:
        abstract = True
        default_manager_name = "objects"
        base_manager_name = "objects"

    def save(self, *args, **kwargs):
        if not hasattr(self, "tenant"):
            self.tenant = get_current_tenant()

        if getattr(self, "tenant", False):
            return super(PolymorphicSingleTenantModelMixin, self).save(*args, **kwargs)
        else:
            raise TenantNotFoundError()


# TODO: This is a fragile abstract base model and should be refactored to be a proper mixin!
#  While its good enough for now, it does require undocumented knowledge.
class PolymorphicMultipleTenantsModelMixin(PolymorphicModel):
    """
    Instances of models inheriting from this are associated with one or more tenant.

    Many Tenant -> Many instances of a Model

    Example:
        Tenant 1              - Instance 1
        Tenant 1 and Tenant 2 - Instance 2
        Tenant 2              - Instance 3
        Tenant 2 and Tenant 3 - Instance 4
        Tenant 3              - Instance 5
    """

    tenants = models.ManyToManyField("tenant.Tenant")

    objects = PolymorphicMultipleTenantModelManager()

    tenant_objects = PolymorphicMultipleTenantModelManager()
    original_manager = PolymorphicManager()

    class Meta:
        abstract = True
        default_manager_name = "objects"
        base_manager_name = "objects"

    # TODO: This doesnt look like safe behaviour, automatically adding the tenant if we have the object?
    def save(self, *args, **kwargs):
        tenant = get_current_tenant()

        if tenant:
            instance = super(PolymorphicMultipleTenantsModelMixin, self).save(*args, **kwargs)
            self.tenants.add(tenant)
            return instance
