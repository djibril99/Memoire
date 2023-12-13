from django.shortcuts import render , redirect

from .models import Marchandise, Livraison
from gestion_utilisateurs.models import Client, Livreur,Utilisateur
from gestion_notifications.models import Notification

from .forms import LivraisonMarchandiseForm
#ajouter la gestion des erreurs pour le template
from django.contrib import messages
#convertir les coordonnees en adresse
from gestion_utilisateurs.views import obtenir_adresse

#views pour les livreurs
def mes_livraisons_livreur(request):
        id_livreur = request.session['user_id']
        user = Utilisateur.objects.get(id=id_livreur)
        livreur = Livreur.objects.get(user=user)
        
        #recuper la liste de ses livraisons postuler , terminées , en cours, 
        
        liste_livraison_en_cours = [(livraison , obtenir_adresse(latitude=livraison.latitude_depart, longitude=livraison.longitude_depart) ,obtenir_adresse(latitude=livraison.latitude_arrivee, longitude=livraison.longitude_arrivee) ) for livraison in Livraison.objects.filter(livreur=livreur, etat_livraison=False)]
        liste_livraison_terminee = [(livraison , obtenir_adresse(latitude=livraison.latitude_depart, longitude=livraison.longitude_depart) ,obtenir_adresse(latitude=livraison.latitude_arrivee, longitude=livraison.longitude_arrivee) ) for livraison in Livraison.objects.filter(livreur=livreur, etat_livraison=True)]
        liste_livraison_postulee = [(notification , obtenir_adresse(latitude=notification.livraison.latitude_depart, longitude=notification.livraison.longitude_depart) ,obtenir_adresse(latitude=notification.livraison.latitude_arrivee, longitude=notification.livraison.longitude_arrivee) ) for notification in Notification.objects.filter(postulation__livreur=livreur , livraison__livreur=None)]
        context = {}
        if len(liste_livraison_en_cours) > 0:
                context['liste_livraison_en_cours'] = liste_livraison_en_cours
        if len(liste_livraison_terminee) > 0:
                context['liste_livraison_terminee'] = liste_livraison_terminee
        if len(liste_livraison_postulee) > 0:
                context['liste_livraison_postulee'] = liste_livraison_postulee
        return render(request, 'gestion_commandes/livreur/liste_livraison_livreur.html', context)
        
        
#["////////////////////////////"]

def livraison_user_connecte(request):
        id_user = request.session['user_id']
        if id_user :
                user = Utilisateur.objects.get(id=id_user)
                if user.type_utilisateur == 'client':
                        client = Client.objects.get(user=user)
                        """mode postulation"""
                        liste_livraison_en_attente = [(notification , obtenir_adresse(latitude=notification.livraison.latitude_depart, longitude=notification.livraison.longitude_depart) ,obtenir_adresse(latitude=notification.livraison.latitude_arrivee, longitude=notification.livraison.longitude_arrivee) ) for notification in Notification.objects.filter(livraison__marchandise__client=client)]
                        liste_livraison_en_cours = [(livraison , obtenir_adresse(latitude=livraison.latitude_depart, longitude=livraison.longitude_depart) ,obtenir_adresse(latitude=livraison.latitude_arrivee, longitude=livraison.longitude_arrivee) ) for livraison in Livraison.objects.filter(marchandise__client=client, etat_livraison=False).exclude(livreur=None)]
                        liste_livraison_terminee = [(livraison , obtenir_adresse(latitude=livraison.latitude_depart, longitude=livraison.longitude_depart) ,obtenir_adresse(latitude=livraison.latitude_arrivee, longitude=livraison.longitude_arrivee) ) for livraison in Livraison.objects.filter(marchandise__client=client, etat_livraison=True)]
                        
                        context = {}
                        if len(liste_livraison_en_cours) > 0:
                                context['liste_livraison_en_cours'] = liste_livraison_en_cours
                        if len(liste_livraison_terminee) > 0:
                                context['liste_livraison_terminee'] = liste_livraison_terminee
                        if len(liste_livraison_en_attente) > 0:
                                context['liste_livraison_en_attente'] = liste_livraison_en_attente
                        return render(request, 'gestion_commandes/client/liste_livraison_client.html', context)
                       
                #pour le livreur afficher la liste des livraisons qu il peut effectuer s il n'est pas en livraison
                elif user.type_utilisateur == 'livreur':
                       return mes_livraisons_livreur(request)
                
        else:
                return redirect('gestion_utilisateurs:index')

def create_livraison(request):
        if request.method == 'POST':
                # Créez une instance du formulaire avec les données POST
                form = LivraisonMarchandiseForm(request.POST, request.FILES)
                if form.is_valid():
                # Enregistrez la marchandise
                        id_user = request.session['user_id']
                        user = Utilisateur.objects.get(id=id_user)   
                        client = Client.objects.get(user=user)
                        
                        livraison = form.save(commit=True, client=client)
                        
                        notification = Notification(livraison=livraison)
                        notification.save()
                        return redirect('gestion_commandes:mes_livraisons')
        
        form = LivraisonMarchandiseForm()

        return render(request, 'gestion_commandes/client/creer_livraison.html', {'form': form})

def affecter_livraison(request, id_livreur):
        livreur = Livreur.objects.get(id=id_livreur)
        if request.method == 'POST':
                form = LivraisonMarchandiseForm(request.POST, request.FILES)
                if form.is_valid():
                        user = Utilisateur.objects.get(id=request.session['user_id'])
                        
                        client = Client.objects.get(user=user)
                        form.save(commit=True, client=client, livreur=livreur)
                        return redirect('gestion_commandes:mes_livraisons')
                else:
                        errors = form.errors
                        for field , error in errors.items():
                                messages.error(request, f"{field} : {error}")
        form = LivraisonMarchandiseForm()
        return render(request, 'gestion_commandes/client/creer_livraison.html', {'form': form, 'livreur':livreur})

#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------Fonctions pour le livreur-----------------------------------------------------------------------------------------

#ajouter un context pour fire la difference

def detail_livraison(request , id_livraison):
        livraison = Livraison.objects.get(id=id_livraison)
        notification = Notification.objects.get(livraison = livraison)
        user = Utilisateur.objects.get(id=request.session['user_id'])
        if not notification : 
                return redirect('gestion_commandes:mes_livraisons')
        
        position_depart = obtenir_adresse(latitude=notification.livraison.latitude_depart, longitude=notification.livraison.longitude_depart)
        position_arrivee = obtenir_adresse(latitude=notification.livraison.latitude_arrivee, longitude=notification.livraison.longitude_arrivee)
        context = {
                'notification':notification,
                'position_depart':position_depart,
                'position_arrivee':position_arrivee,
                }
        return render(request, f'gestion_commandes/{user.type_utilisateur}/detail_livraison.html', context)
        
#terminer une livraison
def validation_livraison(request , id_livraison):
        livraison = Livraison.objects.get(id=id_livraison)
        user = Utilisateur.objects.get(id=request.session['user_id'])
        if request.method == 'POST':
                if request.POST.get('code_validation'):
                        code_validation = request.POST.get('code_validation')
                        if code_validation == livraison.code_validation:
                                livraison.etat_livraison = True
                                #liberer le livreur
                                livraison.livreur.on_mission = False
                                livraison.livreur.save()
                                livraison.save()
                                messages.success(request, "Livraison effectuée avec succès")
                        else:
                                messages.error(request, "Code de validation incorrect")
                                
        return redirect('gestion_commandes:mes_livraisons_livreur')
