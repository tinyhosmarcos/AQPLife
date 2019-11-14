from django.urls import path
from . import views
app_name='documentacion'
urlpatterns = [
	path('',views.IndexView.as_view(),name='index'),
	
]