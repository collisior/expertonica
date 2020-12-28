from django.db import models

# Create your models here.

# class Url(models.Model):
#     """ Model representing url """
#     url = models.URLField(blank=False)

#     def __str__(self):
#         """String for representing the Model object."""
#         return self.url

class WebResult(models.Model):
    """ Model representing website check result"""
    url = models.CharField(primary_key=True, unique=True, blank=False, max_length=1000)
    http_code = models.CharField(max_length=250, blank=True)
    datetime = models.DateTimeField(auto_now_add=True, blank=False)
    ip = models.CharField(max_length=100, blank=True)
    timeout = models.FloatField(blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.url + "\nhttp_code: " + str(self.http_code) + "\ndate_time: " + str(self.datetime) +"\nip: " + self.ip + "\ntimeout: " + str(self.timeout)