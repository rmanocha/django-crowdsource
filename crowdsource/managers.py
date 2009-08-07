from django.db import models
from django.contrib.contenttypes.models import ContentType

class CrowdSourcedEntryManager(models.Manager):
    def all_for_model(self, model):
        """
        Queryset for all crowd sourced entries for a particular model
        
        model -- Model instance we need the queryset for
        """
        ct = ContentType.objects.get_for_model(model)
        return self.get_query_set().filter(content_type = ct, object_id = model._get_pk_val())
        
    def verified_for_model(self, model):
        """
        Queryset for verified crowd sourced entries for a particular model
        
        model -- Model instance we need the queryset for
        """
        ct = ContentType.objects.get_for_model(model)
        return self.get_query_set().filter(content_type = ct, object_id = model._get_pk_val(), verified = True)
