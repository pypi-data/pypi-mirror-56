djangocms-currentuser-field
===========================

An extension to the Aldryn Forms plugin that adds a Current User form field type.  If there is a valid logged-in user session (request.user), that user's information will be saved along with the form submission.

When you build your form, you can select to save the user's:

* User ID
* Username
* Email Address
* Full Name

Installation
------------

1. Install via pip::

    pip install djangocms-currentuser-field
  
2. Add to your ``INSTALLED_APPS`` (in ``settings.py``)::

    INSTALLED_APPS = (
    ...
     'djangocms-currentuser-field',
    ...
    )

    # Optional, if you'd like to use a subclass (1:1 relationship) attached
    # to user for the user id field, specify below
    CURRENTUSER_FIELD_USER_SUBCLASS = 'staff'
        
3. Run migrations::

    python manage.py migrate djangocms-current-user

4. "Current User Field" should now be available as a plugin in the CMS when you build a form!