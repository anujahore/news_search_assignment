from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Article_Source(models.Model):
    new_id = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=200, null=True)
    
    class Meta:
        db_table = "article_source"

class Articles_db(models.Model):
    author = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(max_length=200, null=True)
    url = models.URLField(max_length=500, null=True)
    urlToImage = models.URLField(max_length=500, null=True)
    publishedAt = models.DateTimeField(null=True)
    content = models.TextField(max_length=2000, null=True)
    key_word = models.CharField(max_length=50, null=True)
    user_search_time = models.DateTimeField(auto_now_add=True)
    
    source = models.ForeignKey(Article_Source, on_delete=models.SET_NULL, null=True)
    users = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = "aticles_db"
        
    def __str__(self):
        return f"{self.publishedAt}"
    
# class Article_Source(models.Model):
#     new_id = models.CharField(max_length=50, null=True)
#     name = models.CharField(max_length=200, null=True)
#     article = models.ForeignKey(Articles_db, on_delete=models.CASCADE)
    
#     class Meta:
#         db_table = "article_source"
    



    # {
    #     "source": {
    #         "id": "null",
    #         "name": "Moneycontrol"
    #     },
    #     "author": "Moneycontrol News",
    #     "title": "PM Modi's MP Visit LIVE: PM Modi to unveil development projects in Madhya Pradesh and Chhattisgarh, ahead of upcoming elections - Moneycontrol",
    #     "description": "2023 Tata Nexon Facelift Launch LIVE: As part of TATA.ev's rebranding efforts, the 2023 Tata Nexon EV is now presented with the stylized name &quot;Nexon.ev.&quot; Stay tuned for more updates.",
    #     "url": "https://www.moneycontrol.com/news/automobile/latest-daily-news-live-india-world-current-breaking-updates-37-11364521.html",
    #     "urlToImage": "https://images.moneycontrol.com/static-mcnews/2023/09/7-Tata-Nexon-770x433.jpg",
    #     "publishedAt": "2023-09-14T04:12:33Z",
    #     "content": "The Chhattisgarh East Rail Project Phase-I is a vital component of the PM Gati Shakti-National Master Plan for multi-modal connectivity. It includes a 124.8 km rail line stretching from Kharsia to Dh… [+391 chars]"
    # },