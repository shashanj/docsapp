from django.db import models
from customer.models import Customer
from driver.models import Driver

# Create your models here.
class Ride(models.Model):
    id = models.AutoField(primary_key=True)
    lat = models.CharField(max_length=10)
    long = models.CharField(max_length=10)
    customer = models.ForeignKey(Customer)
    createts = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'ride_request'


class RideDriverEvent(models.Model):
    id = models.AutoField(primary_key=True)
    ride_id = models.ForeignKey(Ride)
    driver_id = models.ForeignKey(Driver)
    status = models.IntegerField(default=0)
    createts = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'ride_driver_event'


class RideDriver(models.Model):
    ride_id = models.OneToOneField(Ride)
    driver_id = models.ForeignKey(Driver)
    status = models.IntegerField(default=0)
    createts = models.DateTimeField(auto_now_add=True)
    last_updatets = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        event = RideDriverEvent()
        event.ride_id = self.ride_id
        event.status = self.status
        event.createts = self.createts
        event.driver_id = self.driver_id
        event.save()
        super(RideDriver, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'ride_driver'