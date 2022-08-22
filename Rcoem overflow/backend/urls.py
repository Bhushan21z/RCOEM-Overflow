from django.contrib import admin
from django.urls import path

from . import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth import views as auth_views
# from myapp import views as myapp_views

schema_view = get_schema_view(
	openapi.Info(
		title="SIH 22 BOTS WITH BRAINS",
		default_version='v1',
		description="SMART INDIA HACKATHON 2022 PROJECT BACKEND",
	),
	public=True,
	permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
	path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
	path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


	path('register',views.register),
	path('login',views.login),
    path('city_api',views.city_api),
    path('city_increment',views.city_increment),

]
