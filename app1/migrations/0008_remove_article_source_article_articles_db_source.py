# Generated by Django 4.2.5 on 2023-09-17 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_alter_articles_db_user_search_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article_source',
            name='article',
        ),
        migrations.AddField(
            model_name='articles_db',
            name='source',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.article_source'),
        ),
    ]
