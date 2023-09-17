# Generated by Django 4.2.5 on 2023-09-17 14:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app1', '0009_articles_db_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles_db',
            name='source',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.article_source'),
        ),
        migrations.AlterField(
            model_name='articles_db',
            name='users',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
