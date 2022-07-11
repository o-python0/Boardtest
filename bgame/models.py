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
    descrption = models.TextField(verbose_name="おすすめポイント", blank=True, default="")
    weight = models.CharField(verbose_name="重さ", max_length=50, choices=WEIGHT, null=True, blank=True)
    
    want_play = models.ManyToManyField(User, through="WantPlay", through_fields=("bgame", "user"), related_name="wantplays")
    interest = models.ManyToManyField(User, through="Interest", through_fields=("bgame", "user"), related_name="interests")

    image = models.ImageField(verbose_name="画像", blank=True, null=True, default=None)
    min_play = models.IntegerField(verbose_name="最低プレイ人数", default=2)

    class Meta:
        verbose_name = "ボードゲーム"
        verbose_name_plural = "ボードゲーム"

    def __str__(self):
        return self.title



class WantPlay(models.Model):
    bgame = models.ForeignKey(Bgame, models.CASCADE, related_name="wantplay_bgame")
    user = models.ForeignKey(User, models.CASCADE, related_name="wantplay_user")
    is_match = models.BooleanField(default=False)


    class Meta:
        verbose_name = "遊んでみたい"
        verbose_name_plural = "遊んでみたい"

    def __str__(self):
        return self.bgame.title



class Interest(models.Model):
    bgame = models.ForeignKey(Bgame, models.CASCADE, related_name="interest_bgame")
    user = models.ForeignKey(User, models.CASCADE, related_name="interest_user")


    class Meta:
        verbose_name = "興味あり"
        verbose_name_plural = "興味あり"

        constraints = [
            models.UniqueConstraint(
                fields=["bgame", "user"],
                name="interest_unique"
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