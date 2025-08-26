from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path("card/<str:name>/", views.card, name="card"),
    path("compare_redirect/<str:left_name>/", views.compare_redirect,
         name="compare_redirect"),
    path("compare/<str:left_name>/<str:right_name>/",
         views.compare, name="compare"),
    path("add/<str:card>/<int:deck_id>/", views.add, name="add"),
    path("add/<str:card>/", views.add, name="add"),
    path("deck/<int:id>/", views.deck, name="deck"),
    path("remove/<int:deck_id>/<int:card_id>/", views.remove, name="remove"),
]
