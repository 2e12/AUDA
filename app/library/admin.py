from django.contrib import admin

from library.models import Track


class LibAdmin(admin.ModelAdmin):
    pass


admin.site.register(Track, LibAdmin)