from django.contrib import admin

from .models import GroupMapping


class GroupMappingAdmin(admin.ModelAdmin):
    pass


admin.site.register(GroupMapping, GroupMappingAdmin)
