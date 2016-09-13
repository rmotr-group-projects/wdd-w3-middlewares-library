from jsonfield import JSONField

from django.db import models


class RequestLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10)
    duration_in_seconds = models.IntegerField()
    code = models.IntegerField()
    url = models.CharField(max_length=100)
    full_url = models.CharField(max_length=200)
    ip = models.CharField(max_length=50)
    get_params = JSONField()
    user_agent = models.CharField(max_length=200, blank=True, null=True)
    query_count = models.IntegerField()
    
class ExceptionLog(models.Model):
    type_of_exception = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
