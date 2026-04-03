# models.py
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils.text import slugify

class User(AbstractUser):

    ROLE_CHOICES = (
        ("customer", "Customer"),
        ("owner", "Restaurant Owner"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    country_code = models.CharField(max_length=10, unique=True)
    dial_code = models.CharField(max_length=10, blank=True, null=True)
    currency_code = models.CharField(max_length=10, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class City(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="cities"
    )
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("country", "name")

    def __str__(self):
        return f"{self.name} - {self.country.name}"


class Restaurant(models.Model):

    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name="restaurants")
    country = models.ForeignKey(Country,on_delete=models.CASCADE,related_name="restaurants")
    name = models.CharField(max_length=150)
    city =  models.ForeignKey(City,on_delete=models.CASCADE,related_name="restaurants")
    rating = models.FloatField()
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
  
      if not self.slug:
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1

        while Restaurant.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        self.slug = slug

      super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.country.name}"
    
class Food(models.Model):
    restaurant = models.ForeignKey( Restaurant, on_delete=models.CASCADE,related_name="foods")
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
    
    
class Order(models.Model):

    customer = models.ForeignKey(User,on_delete=models.CASCADE,related_name="customer_orders")
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name="restaurant_orders")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20,default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    

class OrderItem(models.Model):

    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    food = models.ForeignKey(Food,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    
    
    