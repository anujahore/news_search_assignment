# Generated by Django 4.2.5 on 2023-09-16 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_articles_db_user_search_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles_db',
            name='user_search_time',
            field=models.DateField(auto_now_add=True),
        ),
    ]
