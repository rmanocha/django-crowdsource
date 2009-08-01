# django-crowdsource

django-crowdsource (for the lack of a better name) is an application to allow the users of your site to enter custom defined (url)fields for any object on your site.

As an example, say you have a list of objects representing the members of Congress. You can define fields such as Twitter stream, Home Page, Blog, Blog RSS Feed etc. django-crowdsource would then create a form for you which you can present to your users, allowing them to fill out one or all of these fields. These urls, upon the form's submission, will be saved to your database waiting to be verified by an admin.

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

The first setting defines the module where the custom form class lives (so crowdsource.forms for example).
The second setting defines the name of the form class to use (so CrowdSourcedEntryForm for example).

### urls.py

You will need to add crowdsource.urls to your global URLConf. For example:

   (r'crowdsource/', include('crowdsource.urls')), 

## Usage Instructions
