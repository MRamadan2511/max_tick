from django.db import models

class Ticket(models.Model):
    description = models.TextField('Description', blank=True, null=True)
    post_image= models.ImageField(upload_to='image/post' ,blank=True, null=True,)