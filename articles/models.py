from django.db import models
from django.conf import settings

class Article(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #models.CASCADE : 지울때 연결되어 있는 관계 끊어지면 해당 아티클도 지워버리겠다는 뜻

    class Meta:
        ordering = ('-pk',)


class Comment(models.Model):
    # 1:N관계 표현 시, related name 필수
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')

    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-pk', )

