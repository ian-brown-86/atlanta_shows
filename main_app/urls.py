
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('venues/', views.venues_index, name='venues_index'),
    path('venues/<int:venue_id>/', views.venues_detail, name='detail'),
    path('venues/create/', views.VenueCreate.as_view(), name='venues_create'),
    path('venues/<int:pk>/update/', views.VenueUpdate.as_view(), name='venues_update'),
    path('venues/<int:pk>/delete/', views.VenueDelete.as_view(), name='venues_delete'),
    path('venues/<int:venue_id>/add_shows/', views.add_shows, name='add_shows'),
    path('venues/<int:venue_id>/add_photo/', views.add_photo, name='add_photo'),
    path('acounts/signup/', views.signup, name='signup'),
]