from django.contrib import admin
from .models import Amenity, WorkspaceType, Workspace


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(WorkspaceType)
class WorkspaceTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "location", "is_available")
    list_filter = ("is_available", "workspace_type")
    search_fields = ("name", "location")
    filter_horizontal = ("amenities",)
