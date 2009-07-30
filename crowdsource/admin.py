from django.contrib import admin
from django import forms

from crowdsource.models import CrowdSourcedObject, CrowdSourcedEntry

admin.site.register(CrowdSourcedObject)

class CrowdSourcedEntryAdminForm(forms.ModelForm):
    url = forms.URLField(verify_exists = False)

    class Meta:
        model = CrowdSourcedEntry

class CrowdSourcedEntryAdmin(admin.ModelAdmin):
    list_display = ('get_csentry_related_object', 'csobj', 'url', 'verified')
    list_filter = ('verified', )
    form = CrowdSourcedEntryAdminForm

    def get_csentry_related_object(self, obj):
        return "%s" % obj.related_object
    get_csentry_related_object.short_description = 'Related Object'

admin.site.register(CrowdSourcedEntry, CrowdSourcedEntryAdmin)
