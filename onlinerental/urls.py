from django.urls import path
from . import views

app_name='onlinerental'
urlpatterns = [
    path('', views.CitiesListView.as_view(), name='cities_list'),
    path('/<slug:slug>/', views.ApartmentListView.as_view(), name='lesson_list'),
    path('<str:cities>/<str:slug>/create/', views.ApartmentCreateView.as_view(),name='lesson_create'),
    path('<str:cities>/<slug:slug>/', views.ApartmentDetailView.as_view(),name='lesson_detail'),
    path('/update/', views.ApartmentUpdateView.as_view(),name='lesson_update'),
    path('/delete/', views.ApartmentDeleteView.as_view(),name='lesson_delete'),

]
