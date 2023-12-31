# Generated by Django 4.2.5 on 2023-12-10 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_commandes', '0007_remove_livraison_code_prise_marchandise'),
        ('gestion_utilisateurs', '0010_alter_utilisateur_type_utilisateur'),
        ('gestion_notifications', '0005_remove_notification_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='livraison',
        ),
        migrations.CreateModel(
            name='Postulation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('prixPropose', models.FloatField(blank=True, null=True)),
                ('Livraison', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestion_commandes.livraison')),
                ('Livreur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestion_utilisateurs.livreur')),
            ],
        ),
        migrations.AddField(
            model_name='notification',
            name='postulation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestion_notifications.postulation'),
        ),
    ]
