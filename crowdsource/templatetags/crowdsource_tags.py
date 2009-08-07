from django import template
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

import crowdsource

register = template.Library()

class CrowdSourcedEntryFormNode(template.Node):
    def handle_token(cls, parser, token):
        tokens = token.contents.split()
        if tokens[1] != 'for':
            raise template.TemplateSyntaxError("Second argument in %r tag must be 'for'" % tokens[0])

        if len(tokens) == 5:
            if tokens[3] != 'as':
                raise template.TemplateSyntaxError("Third argument in %r must be 'as'" % tokens[0])
            return cls(
                    object_expr = parser.compile_filter(tokens[2]),
                    as_varname = tokens[4],
            )
        elif len(tokens) == 6:
            if tokens[4] != 'as':
                raise template.TemplateSyntaxError("Fourth argument in %r must be 'as'" % tokens[0])
            return cls(
                    ctype = CrowdSourcedEntryFormNode.lookup_content_type(tokens[2], tokens[0]),
                    object_id_expr = parser.compile_filter(tokens[3]),
                    as_varname = tokens[5]
            )
        else:
            raise template.TemplateSyntaxError("%r tag requires 4 or 5 arguments" % tokens[0])

    handle_token = classmethod(handle_token)

    def lookup_content_type(token, tagname):
        try:
            app, model = token.split('.')
            return ContentType.objects.get(app_label = app, model = model)
        except ValueError:
            raise template.TemplateSyntaxError("Third argument in %r must be in the format 'app.model'" % tagname)
        except ContentType.DoesNotExist:
            raise template.TemplateSyntaxError("%r tag has non-existant content-type: '%s.%s'" % (tagname, app, model))

    lookup_content_type = staticmethod(lookup_content_type)

    def __init__(self, ctype = None, object_id_expr = None, object_expr = None, as_varname = None):
        if ctype is None and object_expr is None:
            raise template.TemplateSyntaxError("CrowdSourcedEntry nodes must be given either a literal object or a ctype and object pk.")

        self.as_varname = as_varname
        self.ctype = ctype
        self.object_id_expr = object_id_expr
        self.object_expr = object_expr

    def get_target_ctype_pk(self, context):
        if self.object_expr:
            try:
                obj = self.object_expr.resolve(context)
            except template.VariableDoesNotExist:
                return None, None
            return ContentType.objects.get_for_model(obj), obj.pk
        else:
            return self.ctype, self.object_id_expr.resolve(context, ignore_failures = True)

    def get_form(self, context):
        ctype, object_id = self.get_target_ctype_pk(context)
        if object_id:
            return crowdsource.get_form()(ctype.get_object_for_this_type(pk = object_id))
        else:
            return None

    def render(self, context):
        context[self.as_varname] = self.get_form(context)
        return ''

class RenderCrowdSourcedEntryFormNode(CrowdSourcedEntryFormNode):
    def handle_token(cls, parser, token):
        tokens = token.contents.split()
        if tokens[1] != 'for':
            raise template.TemplateSyntaxError("Second argument in %r tag must be 'for'" % tokens[0])

        if len(tokens) == 3:
            return cls(object_expr = parser.compile_filter(tokens[2]))
        elif len(tokens) == 4:
            return cls(
                ctype = CrowdSourcedEntryFormNode.lookup_content_type(tokens[2], tokens[0]),
                object_id_expr = parser.compile_filter(tokens[3])
            )
        else:
            raise template.TemplateSyntaxError("%r tag requires 2 or 3 arguments" % tokens[0])
    handle_token = classmethod(handle_token)

    def render(self, context):
        ctype, object_id = self.get_target_ctype_pk(context)
        if object_id:
            template_search_list = [
                    "crowdsource/%s/%s/form.html" % (ctype.app_label, ctype.model),
                    "crowdsource/%s/form.html" % ctype.app_label,
                    "crowdsource/form.html"
            ]
            cs_form = self.get_form(context)
            context.push()
            formstr = render_to_string(template_search_list, {"form" : cs_form, "object" : cs_form.target_object}, context)
            context.pop()
            return formstr
        else:
            return ''

def get_crowdsourcedentry_form(parser, token):
    return CrowdSourcedEntryFormNode.handle_token(parser, token)

def render_crowdsourcedentry_form(parser, token):
    return RenderCrowdSourcedEntryFormNode.handle_token(parser, token)

register.tag(get_crowdsourcedentry_form)
register.tag(render_crowdsourcedentry_form)
