from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username if self.user else self.email

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='product/images/')
    category = models.CharField(max_length=100 ,null=True)
    description = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True , blank=True)
    products = models.ManyToManyField(Product, through='CartItem')
    # quantity = models.PositiveIntegerField(default=1)
    # created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.user )

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(null = True)
    comment = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='review/',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Review by {self.user.username} on {self.product.name}'