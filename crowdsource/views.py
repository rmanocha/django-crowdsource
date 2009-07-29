from django.http import HttpResponseRedirect, HttpResponse, Http404
from django import http
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from crowdsource.forms import CrowdSourcedEntryForm

class CommentPostBadRequest(http.HttpResponseBadRequest):
    """
    Response returned when a comment post is invalid. If ``DEBUG`` is on a
    nice-ish error message will be displayed (for debugging purposes), but in
    production mode a simple opaque 400 page will be displayed.
    """
    def __init__(self):
        super(CommentPostBadRequest, self).__init__()

def post_csentry(request, next = None):
    data = request.POST.copy()

    next = data.get("next", next)

    ctype = data.get("content_type")
    object_id = data.get("object_id")
    if ctype is None or object_id is None:
        return Http404
    try:
        model = models.get_model(*ctype.split(".", 1))
        target = model._default_manager.get(pk = object_id)
    except TypeError:
        return CommentPostBadRequest()
    except AttributeError:
        return CommentPostBadRequest()
    except ObjectDoesNotExist:
        return CommentPostBadRequest()

    csentry_form = CrowdSourcedEntryForm(target, data = data)

    if csentry_form.is_valid():
        csentry_form.save()
        if next:
            return HttpResponseRedirect(next)
        else:
            return HttpResponseRedirect(target.get_absolute_url())
    else:
        return CommentPostBadRequest()

post_csentry = require_POST(post_csentry)

