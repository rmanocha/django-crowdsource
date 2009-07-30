from django.contrib import admin

from crowdsource.models import CrowdSourcedObject, CrowdSourcedEntry

class CrowdSourcedObjectAdmin(admin.ModelAdmin):
    pass

admin.site.register(CrowdSourcedObject, CrowdSourcedObjectAdmin)

class CrowdSourcedEntryAdmin(admin.ModelAdmin):
    exclude = ('content_type', 'object_id')

admin.site.register(CrowdSourcedEntry, CrowdSourcedEntryAdmin)
