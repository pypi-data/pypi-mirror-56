from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from django.core.handlers.wsgi import WSGIRequest
from dj_pony.tenant.models import Tenant, TenantSite
from dj_pony.tenant.settings import get_setting, cache_name, use_cache
from dj_pony.tenant.exceptions import TenantNotFoundError
from django.core.cache import caches, InvalidCacheBackendError


# Setup our tenant library specific cache.
try:
    if use_cache():
        # TODO: Log some sensible info here.
        TENANT_CACHE = caches[cache_name()]
        # TODO: Check the type and warn if not using LocMem, or similar.
    else:
        # TODO: Log some sensible info here.
        TENANT_CACHE = None
except InvalidCacheBackendError:
    # TODO: Raise some sensible warning here.
    TENANT_CACHE = None


# Cache config/tools alternatives...
# https://github.com/Yiling-J/django-cacheme
# https://django-memoize.readthedocs.io/en/latest/
# https://github.com/django/django/blob/0284a26af9d9adc58647df1a684b76969cf258e9/django/http/request.py#L40
# Need to build some kind of cache key from the request object... but its probably best to cache it this way.
# https://en.wikipedia.org/wiki/List_of_HTTP_header_fields
# date is a good field to help make this easier... but django's request factory doesnt appear to create with dates.
# https://docs.djangoproject.com/en/2.2/_modules/django/test/client/#RequestFactory
#
# https://stackoverflow.com/questions/50498944/django-requestfactory-add-http-x-forwarded-for
# https://djangosnippets.org/snippets/850/


def retrieve_by_domain(request: WSGIRequest):
    try:
        return get_current_site(request).tenant_site.tenant
    except (TenantSite.DoesNotExist, Site.DoesNotExist):
        return None
    # TODO: I'm not sure how to reach this branch.
    #  Since a TenantSite must have a Tenant and uses cascading deletes.
    except Tenant.DoesNotExist:  # pragma: no cover
        raise TenantNotFoundError()


def retrieve_by_http_header(request: WSGIRequest):

    try:
        tenant_http_header = (
            "HTTP_" + get_setting("TENANT_HTTP_HEADER").replace("-", "_").upper()
        )

        # TODO: This probably needs a try except block for safety.
        if TENANT_CACHE is not None:
            cache_key = f'dj-pony.tenant_retrieve-by-http-header_<WSGIRequest:{hex(id(request))}>'
            tenant = TENANT_CACHE.get(cache_key, None)
            if tenant is None:
                tenant = Tenant.objects.get(slug=request.META[tenant_http_header])
                TENANT_CACHE.set(cache_key, tenant)
        else:
            tenant = Tenant.objects.get(slug=request.META[tenant_http_header])

        return tenant
    except LookupError:
        return None
    except Tenant.DoesNotExist:
        raise TenantNotFoundError()


def retrieve_by_session(request: WSGIRequest):
    try:
        # TODO: should this key be configurable? Not sure how much work that is...
        tenant_slug = request.session["tenant_slug"]

        # TODO: This probably needs a try except block for safety.
        if TENANT_CACHE is not None:
            cache_key = f'dj-pony.tenant_retrieve-by-session_<WSGIRequest:{hex(id(request))}>'
            tenant = TENANT_CACHE.get(cache_key, None)
            if tenant is None:
                tenant = Tenant.objects.get(slug=tenant_slug)
                TENANT_CACHE.set(cache_key, tenant)
        else:
            tenant = Tenant.objects.get(slug=tenant_slug)
        # return Tenant.objects.get(slug=request.session["tenant_slug"])
        return tenant
    except (AttributeError, LookupError, Tenant.DoesNotExist):
        return None
    # TODO: I think this may be unreachable.
    #  Since a TenantSite must have a Tenant and uses cascading deletes.
    except Tenant.DoesNotExist:  # pragma: no cover
        raise TenantNotFoundError()
