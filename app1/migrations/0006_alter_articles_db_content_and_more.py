# Generated by Django 4.2.5 on 2023-09-17 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_alter_articles_db_user_search_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles_db',
            name='content',
            field=models.TextField(max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='articles_db',
            name='description',
            field=models.TextField(max_length=200, null=True),
        ),
    ]