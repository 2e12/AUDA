from django.contrib import admin
from django.urls import include, path

from api.urls import router

urlpatterns = [
    path("library/", include("library.urls")),
    path('auth/', include('rest_framework.urls')),
    path('v1/', include(router.urls)),
    path("admin/", admin.site.urls),
]

