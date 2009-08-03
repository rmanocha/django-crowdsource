# django-crowdsource

django-crowdsource (for the lack of a better name) is an application to allow the users of your site to enter custom defined (url)fields for any object on your site.

As an example, say you have a list of objects representing the members of Congress. You can define fields such as Twitter stream, Home Page, Blog, Blog RSS Feed etc. ``django-crowdsource`` would then create a form for you which you can present to your users, allowing them to fill out one or all of these fields. These urls, upon the form's submission, will be saved to your database waiting to be verified by an admin.

``django-crowdsource`` is released under the BSD license. See License.txt for more details.

## Requirements

python >= 2.4

django >= 1.0

## Installation

Currently, the only way to install django-crowdsource is to clone the git repository and create a symlink to the django-crowdsource/crowdsource folder to somewhere in your Django project's PYTHONPATH.

To clone the repository, you need to issue the following command:

    git clone git://github.com/rmanocha/django-crowdsource.git

## Quick Setup

### settings.py

Add to INSTALLED_APPS:

    'crowdsource'

Additionally, if you want to define a custom form (instead of using crowdsource.forms.CrowdSourcedEntryForm), add the following two settings:

    'CROWD_SOURCED_ENTRY_FORM_MODULE' = 'custom form module'
    'CROWD_SOURCED_ENTRY_FORM_NAME'   = 'custom form class name'

The first setting defines the module where the custom form class lives (so ``crowdsource.forms`` for example).
The second setting defines the name of the form class to use (so ``CrowdSourcedEntryForm`` for example).

### urls.py

You will need to add crowdsource.urls to your global URLConf. For example:

    (r'crowdsource/', include('crowdsource.urls')), 

## Usage Instructions

``django-crowdsource`` works, for the most part, the same as ``django.contrib.comments``. Templatetags are used
to get a form object (or get the rendered form) and upon submission the relevant entries for the given
object are created.

### Templatetags

Start with loading the templatetags inside your templates

	{% load crowdsource_tags %}

You now have two templatetags you can call. The first is
	
	{% get_crowdsource_entry for obj as csentry_form %}

This tag will return a form object for ``obj`` as ``csentry_form``. You can then use ``csentry_form`` to render the form into your template. You can also call this templatetag like so:

	{% get_crowdsource_entry for [app].[model] [object_id] as [varname] %}

The other templatetag available is:

	{% render_crowdsource_entry for obj %}

This tag renders the relevant form for obj. The template search path to render the form is:

	'crowdsource/{{ app_label }}/{{ model }}/form.html',
	'crowdsource/{{ app_label }}/form.html',
	'crowdsource/form.html'	

You can also call this tag like so:

	{% render_crowdsource_entry for [app].[model] [object.id] %}

This tag passes the ``form`` context variable to the template which can be used to render the form in whatever way you like.

### URLS

The form needs to be submitted to ``post-cs-entry``, so in your template, the form's action should be something like:

	<form method="post" action="{% post-cs-entry %}">
		{{ form }}
	</form>

## Notes

### Forms

The form used by default is ``crowdsource.forms.CrowdSourcedEntryForm``. You can customise this form by defining two settings:

	CROWD_SOURCED_ENTRY_FORM_MODULE
	CROWD_SOURCED_ENTRY_FORM_NAME

See the settings section to see what each does. If you do define a custom form, you should make it inherit from ``crowdsource.forms.CrowdSourcedEntrySecurityForm`` which will take care of all housekeeping for you.
