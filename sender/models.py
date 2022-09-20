from django.db import models


class Mail(models.Model):
	from_addr = models.EmailField(editable=False)
	to_addr = models.EmailField()
	subject = models.CharField(max_length=200)
	body = models.TextField()