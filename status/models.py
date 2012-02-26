from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User

class Status(models.Model):
	status = models.TextField()
	creation_date = models.DateTimeField(default=datetime.now)
	ticketslist = models.CommaSeparatedIntegerField(max_length=200)
	author = models.ForeignKey(User)
	deleted = models.BooleanField()
	latest = models.BooleanField(default=True)

	def __unicode__(self):
		return self.status
	
	def save(self, **kwargs):
		now = datetime.now()
		# When we save we want to mark all other entries 
		# that are older than today as not the latest.
		start = datetime.min.replace(year=now.year, month=now.month, day=now.day)
		end = (start + timedelta(days=1)) - timedelta.resolution
		Status.objects.filter(latest=True, creator=self.creator).filter(
			creation_date__range=(start, end)).update(latest=False)
		super(Status, self).save(**kwargs)

