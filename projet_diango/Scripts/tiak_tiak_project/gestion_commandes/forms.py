from django import forms
from gestion_utilisateurs.models import Livreur, Client, Utilisateur
from .models import Marchandise, Livraison
import random
import string


class LivraisonMarchandiseForm(forms.ModelForm):
    class Meta:
        model = Livraison
        fields = ['longitude_depart', 'latitude_depart', 'longitude_arrivee', 'latitude_arrivee']

    # Champs pour la marchandise
    photo_marchandise = forms.ImageField()
    description = forms.CharField(max_length=500, widget=forms.Textarea)

    def clean(self):
        cleaned_data = super().clean()
        # Vous pouvez ajouter des validations personnalisées ici si nécessaire

    # GÉNÉRER UN CODE ALÉATOIRE DE 150 CARACTÈRES
    def generer_code_aleatoire(self, taille=10):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=taille))

    def save(self, commit=True, client=None , livreur=None):
        # Enregistrez la marchandise en premier pour obtenir son ID
        marchandise = Marchandise(photo=self.cleaned_data['photo_marchandise'], description=self.cleaned_data['description'], client=client)
        marchandise.save()

        # Ensuite, enregistrez la livraison avec l'ID de la marchandise
        livraison = Livraison(
            marchandise=marchandise,
            longitude_depart=self.cleaned_data['longitude_depart'],
            latitude_depart=self.cleaned_data['latitude_depart'],
            longitude_arrivee=self.cleaned_data['longitude_arrivee'],
            latitude_arrivee=self.cleaned_data['latitude_arrivee'],
            code_validation=self.generer_code_aleatoire(),
        )
        if livreur:
                livraison.livreur = livreur

        if commit:
            livraison.save()

        return livraison
