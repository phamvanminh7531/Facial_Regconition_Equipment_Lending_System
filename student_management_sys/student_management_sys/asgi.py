"""
ASGI config for student_management_sys project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_sys.settings')

# application = get_asgi_application()



import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter

from api.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_sys.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": application,
    "websocket": URLRouter(websocket_urlpatterns),
})