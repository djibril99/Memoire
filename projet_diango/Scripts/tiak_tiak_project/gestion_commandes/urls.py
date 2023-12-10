from django.urls import path
from . import views
app_name = 'gestion_commandes'

urlpatterns = [
        path('', views.livraison_user_connecte, name='mes_livraisons'),
        #creer une nouvelle livraison
        path('creer_livraison/', views.create_livraison, name='creer_livraison'),
        path('detail_livraison/<int:id_livraison>/', views.detail_livraison, name='detail_livraison'),
        #affecter une livraison a un livreur
        path('affecter_livraison/<int:id_livreur>/', views.affecter_livraison, name='affecter_livraison'),
        #pour les livreurs
        path('mes_livraisons_livreur/', views.mes_livraisons_livreur, name='mes_livraisons_livreur'),
        path('validation_livraison/<int:id_livraison>/', views.validation_livraison, name='validation_livraison'),
]