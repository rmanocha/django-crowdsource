from django.contrib import admin

from crowdsource.models import CrowdSourcedObject, CrowdSourcedEntry

class CrowdSourcedObjectAdmin(admin.ModelAdmin):
    pass

admin.site.register(CrowdSourcedObject, CrowdSourcedObjectAdmin)

class CrowdSourcedEntryAdmin(admin.ModelAdmin):
    pass

admin.site.register(CrowdSourcedEntry, CrowdSourcedEntryAdmin)
