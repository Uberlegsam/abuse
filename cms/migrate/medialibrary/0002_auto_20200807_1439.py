# Generated by Django 3.0 on 2020-08-07 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medialibrary', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediafiletranslation',
            name='language_code',
            field=models.CharField(choices=[('ru', 'Russian'), ('en', 'English')], default='ru', max_length=10, verbose_name='language'),
        ),
    ]
