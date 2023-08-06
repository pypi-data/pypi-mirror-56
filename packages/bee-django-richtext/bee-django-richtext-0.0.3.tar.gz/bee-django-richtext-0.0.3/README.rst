========================
richtext
========================

Quick start
-----------

1. Add "message" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'bee_django_richtext.apps.BeeDjangoRichtextConfig',
    )

2. Include the crm URLconf in your project urls.py like this::

    from django.conf.urls import include, url
    ...
    url(r'^bee_django_richtext/', include('bee_django_richtext.urls')),


3. Run `python manage.py makemigrations`,`python manage.py migrate` to create the richtext models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a message (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/wiki/ to participate in the message.

6. Use
from bee_django_richtext.custom_fields import RichTextField
info = RichTextField(app_name=None, model_name=None, emotion=False, img=False, undo_redo=False, text_min_length=5,image_max_size=2)