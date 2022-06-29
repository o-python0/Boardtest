from django.db import models

from django.contrib.auth.models import User


WEIGHT = (
    ('軽量級', '軽量級'),
    ('中量級', '中量級'),
    ('重量級', '重量級'),
)



class Bgame(models.Model):
    title = models.CharField(verbose_name="タイトル", max_length=50)
    content = models.TextField(verbose_name="ゲーム概要")
    descrption = models.TextField(verbose_name="説明", blank=True, default="")
    weight = models.CharField(verbose_name="重さ", max_length=50, choices=WEIGHT, null=True, blank=True)
    
    want_play = models.ManyToManyField(User, through="WantPlay", through_fields=("bgame", "user"))

    image = models.ImageField(verbose_name="画像", blank=True, null=True, default=None)
    min_play = models.IntegerField(verbose_name="最低プレイ人数", default=2)

    class Meta:
        verbose_name = "ボードゲーム"
        verbose_name_plural = "ボードゲーム"

    def __str__(self):
        return self.title


class WantPlay(models.Model):
    bgame = models.ForeignKey(Bgame, models.DO_NOTHING)
    user = models.ForeignKey(User, models.CASCADE)


    class Meta:
        verbose_name = "遊んでみたい"
        verbose_name_plural = "遊んでみたい"

        constraints = [
            models.UniqueConstraint(
                fields=["bgame", "user"],
                name="wantplay_unique"
            ),
        ]

    def __str__(self):
        return self.bgame.title




class Comment(models.Model):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    bgame = models.ForeignKey(Bgame, on_delete=models.CASCADE, default=None, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)


    class Meta:
        verbose_name = "コメント"
        verbose_name_plural = "コメント"

    def __str__(self):
        return self.content