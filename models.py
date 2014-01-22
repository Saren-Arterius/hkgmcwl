from django.db import models

# Create your models here.
class Whitelist(models.Model):
    hkg_uid = models.IntegerField()
    ip = models.CharField(max_length=12)
    mc_name = models.CharField(max_length=20)
    time = models.IntegerField()
    def __str__(self):
        return "{0} - {1}".format(self.hkg_uid, self.mc_name)