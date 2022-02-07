# Generated by Django 4.0.1 on 2022-02-06 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('labocore', '0007_alter_composants_auteur_alter_composants_vetement'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vetement', models.CharField(max_length=300)),
                ('sexe', models.CharField(max_length=300)),
                ('auteur', models.CharField(max_length=300)),
                ('top_model', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='CaoComposant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=300)),
                ('cao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labocore.cao')),
            ],
        ),
        migrations.CreateModel(
            name='CaoModelImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images')),
            ],
        ),
        migrations.CreateModel(
            name='CaoImageComposant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(max_length=500)),
                ('caocomposant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labocore.caocomposant')),
            ],
        ),
    ]