
from dj_pony.tenant.helpers import get_current_tenant
from polymorphic.managers import PolymorphicManager


# noinspection DuplicatedCode
class PolymorphicSingleTenantModelManager(PolymorphicManager):
    def get_original_queryset(self, *args, **kwargs):
        return super(PolymorphicSingleTenantModelManager, self).get_queryset(*args, **kwargs)

    def get_queryset(self, tenant=None, *args, **kwargs):
        if not tenant:
            tenant = get_current_tenant()
            if tenant:
                return (
                    super(PolymorphicSingleTenantModelManager, self)
                    .get_queryset(*args, **kwargs)
                    .filter(tenant=tenant)
                )
            else:
                return (
                    super(PolymorphicSingleTenantModelManager, self)
                    .get_queryset(*args, **kwargs)
                    .none()
                )
        else:
            return (
                super(PolymorphicSingleTenantModelManager, self)
                .get_queryset(*args, **kwargs)
                .filter(tenant=tenant)
            )

    def bulk_create(self, objs, batch_size=None, ignore_conflicts=False):
        # TODO: Something here to avoid silently losing changes in bulk create calls...
        # print()
        print("Hit Bulk Create")
        # print()
        super(PolymorphicSingleTenantModelManager, self).bulk_create(
            objs, batch_size=batch_size, ignore_conflicts=ignore_conflicts
        )

    def bulk_update(self, objs, fields, batch_size=None):
        # TODO: Something here to avoid silently losing changes in bulk update calls...
        # print()
        print("Hit Bulk Update")
        # print()
        super(PolymorphicSingleTenantModelManager, self).bulk_update(
            objs, fields, batch_size=batch_size
        )


# noinspection DuplicatedCode
class PolymorphicMultipleTenantModelManager(PolymorphicManager):
    def get_original_queryset(self, *args, **kwargs):
        return super(PolymorphicMultipleTenantModelManager, self).get_queryset(*args, **kwargs)

    def get_queryset(self, tenant=None, *args, **kwargs):
        if not tenant:
            tenant = get_current_tenant()
            if tenant:
                return (
                    super(PolymorphicMultipleTenantModelManager, self)
                    .get_queryset(*args, **kwargs)
                    .filter(tenants=tenant)
                )
            else:
                return (
                    super(PolymorphicMultipleTenantModelManager, self)
                    .get_queryset(*args, **kwargs)
                    .none()
                )
        else:
            return (
                super(PolymorphicMultipleTenantModelManager, self)
                .get_queryset(*args, **kwargs)
                .filter(tenants=tenant)
            )

    def bulk_create(self, objs, batch_size=None, ignore_conflicts=False):
        # TODO: Something here to avoid silently losing changes in bulk create calls...
        # print()
        print("Hit Bulk Create")
        # print()
        super(PolymorphicMultipleTenantModelManager, self).bulk_create(
            objs, batch_size=batch_size, ignore_conflicts=ignore_conflicts
        )

    def bulk_update(self, objs, fields, batch_size=None):
        # TODO: Something here to avoid silently losing changes in bulk update calls...
        # print()
        print("Hit Bulk Update")
        # print()
        super(PolymorphicMultipleTenantModelManager, self).bulk_update(
            objs, fields, batch_size=batch_size
        )
