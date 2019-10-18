from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.BrassinsList.as_view(), name="brassin_list"),
    path('consult-<int:id>/', views.BrassinConsult, name='brassin_consult'),
    path('consult-addingredient<int:id>/', views.BrassinIngredientAdd, name='brassin_ingredient_add'),
    path('consult-<int:id_brassin>/delete-ingredient-<int:pk>/', views.BrassinIngredientDelete.as_view(), name='brassin_ingredient_delete'),
    path('nouveau/', views.BrassinCreate.as_view(), name='brassin_create'),
    path('edit-<int:pk>/', views.BrassinUpdate.as_view(), name='brassin_update'),
    path('supprimer-<int:pk>/', views.BrassinDelete.as_view(), name='brassin_delete'),
    path('recette/', views.RecettesList.as_view(), name="recettes_list"),
    path('recette/consult-<int:id>/', views.RecetteConsult, name='recette_consult'),
    path('recette/consult-addingredient<int:id>/', views.RecetteIngredientAdd, name='recette_ingredient_add'),
    path('recette/consult-<int:id_recette>/delete-ingredient-<int:pk>/', views.RecetteIngredientDelete.as_view(), name='recette_ingredient_delete'),
    path('recette/nouveau/', views.RecetteCreate.as_view(), name='recette_create'),
    path('recette/edit-<int:pk>/', views.RecetteUpdate.as_view(), name='recette_update'),
    path('recette/supprimer-<int:pk>/', views.RecetteDelete.as_view(), name='recette_delete'),
    path('ingredients/', views.IngredientsList.as_view(), name="ingredients_list"),
    path('ingredients/nouveau/', views.IngredientCreate.as_view(), name='ingredient_create'),
    path('ingredients/edit-<int:pk>/', views.IngredientUpdate.as_view(), name='ingredient_update'),
    path('ingredients/supprimer-<int:pk>/', views.IngredientDelete.as_view(), name='ingredient_delete'),
    path('achats/', views.AchatsList.as_view(), name="achats_list"),
    path('achats/nouveau/', views.AchatCreate.as_view(), name='achat_create'),
    path('achats/edit-<int:pk>/', views.AchatUpdate.as_view(), name='achat_update'),
    path('achats/supprimer-<int:pk>/', views.AchatDelete.as_view(), name='achat_delete'),
    path('ventes/', views.VentesList.as_view(), name="ventes_list"),
    path('ventes/nouveau/', views.VenteCreate.as_view(), name='vente_create'),
    path('ventes/edit-<int:pk>/', views.VenteUpdate.as_view(), name='vente_update'),
    path('ventes/supprimer-<int:pk>/', views.VenteDelete.as_view(), name='vente_delete'),
]