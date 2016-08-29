from django.contrib import admin

# Register your models here.
from .models import Collection, Link, Tag


class CollectionModelAdmin(admin.ModelAdmin):
    list_display = ["title","update", "timestamp"]

    class Meta:
        model = Collection


class LinkModelAdmin(admin.ModelAdmin):
    list_display = ["link", "timestamp"]

    class Meta:
        model = Link


class TagModelAdmin(admin.ModelAdmin):
    list_display = ["name", "timestamp"]

    class Meta:
        model = Tag


admin.site.register(Collection, CollectionModelAdmin)
admin.site.register(Link, LinkModelAdmin)
admin.site.register(Tag, TagModelAdmin)