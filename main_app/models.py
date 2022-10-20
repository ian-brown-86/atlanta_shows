from django.db import models
from django.urls import reverse

class Venue(models.Model):
    name = models.CharField(max_length=100)
    loc = models.CharField(max_length=100)
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'venue_id': self.id})


class Shows(models.Model):
    class Meta:
        ordering = ('-date',)

    date = models.DateField()
    band = models.CharField(max_length=30)
    cost = models.SmallIntegerField()

    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.band} on {self.date} for ${self.cost}'

class Photo(models.Model):
    url = models.CharField(max_length=200)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    def __str__(self):
        return f'Photo for venue_id: {self.venue_id} @{self.url}'