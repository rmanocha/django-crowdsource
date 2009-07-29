import time
import datetime

from django import forms
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.hashcompat import sha_constructor

from crowdsource.models import CrowdSourcedObject, CrowdSourcedEntry

class CrowdSourcedEntrySecurityForm(forms.Form):
    content_type  = forms.CharField(widget=forms.HiddenInput)
    object_id     = forms.CharField(widget=forms.HiddenInput)
    timestamp     = forms.IntegerField(widget=forms.HiddenInput)
    security_hash = forms.CharField(min_length=40, max_length=40, widget=forms.HiddenInput)

    def __init__(self, target_object, data = None, initial = None):
        self.target_object = target_object
        if initial is None:
            initial = {}
        initial.update(self.generate_security_data())
        super(CrowdSourcedEntrySecurityForm, self).__init__(data = data, initial = initial)

    def clean_security_hash(self):
        """Check the security hash."""
        security_hash_dict = {
            'content_type' : self.data.get("content_type", ""),
            'object_id' : self.data.get("object_id", ""),
            'timestamp' : self.data.get("timestamp", ""),
        }
        expected_hash = self.generate_security_hash(**security_hash_dict)
        actual_hash = self.cleaned_data["security_hash"]
        if expected_hash != actual_hash:
            raise forms.ValidationError("Security hash check failed.")
        return actual_hash

    def clean_timestamp(self):
        """Make sure the timestamp isn't too far (> 2 hours) in the past."""
        ts = self.cleaned_data["timestamp"]
        if time.time() - ts > (2 * 60 * 60):
            raise forms.ValidationError("Timestamp check failed")
        return ts

    def generate_security_data(self):
        """Generate a dict of security data for "initial" data."""
        timestamp = int(time.time())
        security_dict =   {
            'content_type'  : str(self.target_object._meta),
            'object_id'     : str(self.target_object._get_pk_val()),
            'timestamp'     : str(timestamp),
            'security_hash' : self.initial_security_hash(timestamp),
        }
        return security_dict
    
    def initial_security_hash(self, timestamp):
        """
        Generate the initial security hash from self.content_object
        and a (unix) timestamp.
        """

        initial_security_dict = {
            'content_type' : str(self.target_object._meta),
            'object_id' : str(self.target_object._get_pk_val()),
            'timestamp' : str(timestamp),
          }
        return self.generate_security_hash(**initial_security_dict)

    def generate_security_hash(self, content_type, object_id, timestamp):
        """Generate a (SHA1) security hash from the provided info."""
        info = (content_type, object_id, timestamp, settings.SECRET_KEY)
        return sha_constructor("".join(info)).hexdigest()

class CrowdSourcedEntryForm(CrowdSourcedEntrySecurityForm):
    honeypot = forms.CharField(required = False,
            label = 'If you enter anything in this field your entry'\
                    'will be treated as spam',
            widget = forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(CrowdSourcedEntryForm, self).__init__(*args, **kwargs)

        for csobj in CrowdSourcedObject.objects.all():
            qs = CrowdSourcedEntry.objects.filter(csobj = csobj, content_type = ContentType.objects.get_for_model(self.target_object), object_id = self.target_object._get_pk_val())
            if qs:
                self.fields[csobj.name] = forms.URLField(label = csobj.help_text, required = False, verify_exists = True, widget = forms.TextInput(attrs = {'disabled' : True}), initial = qs.get().url)
            else: 
                self.fields[csobj.name] = forms.URLField(label = csobj.help_text, required = False, verify_exists = True)

    def clean_honeypot(self):
        value = self.cleaned_data["honeypot"]
        if value:
            raise forms.ValidationError(self.fields["honeypot"].label)
        return value

    def save(self):
        for key in self.cleaned_data:
            if self.cleaned_data[key]:
                try:
                    CrowdSourcedEntry.objects.create(
                        csobj = CrowdSourcedObject.objects.get(name = key),
                        content_type = ContentType.objects.get_for_model(self.target_object),
                        object_id = self.target_object._get_pk_val(), 
                        url = self.cleaned_data[key]
                    )
                except CrowdSourcedObject.DoesNotExist:
                    pass
