from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from htmx_demo.core import urls as core_urls

urlpatterns = [
    path("", include(core_urls)),
    path("auth/", include("django.contrib.auth.urls")),
    path("django-admin/", admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if hasattr(settings, "SENTRY_TEST_URL_ENABLED") and settings.SENTRY_TEST_URL_ENABLED:

    def trigger_error(request):
        return 1 / 0

    urlpatterns += [
        path("_trigger-error/", trigger_error),  # type: ignore
    ]
