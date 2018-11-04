from django.db import models

# Create your models here.

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    mobile = models.CharField(max_length=13)
    email = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'customer'