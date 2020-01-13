from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    text = models.CharField(max_length=200)
    datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return " : ".join([
            str(field)
            for field in [
                self.datetime.strftime("%d.%m, %H:%M"),
                self.user,
                self.text
            ]
        ])

    class Meta:
        ordering = ('datetime',)
