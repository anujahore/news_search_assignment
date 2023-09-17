from django.contrib import admin
from .models import Article_Source, Articles_db
# Register your models here.


admin.site.register([Articles_db, Article_Source])
