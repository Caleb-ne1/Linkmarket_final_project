from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    username = None 
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    def __str__(self):
        return self.email
    
 
    
class Business(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def save(self, *args, **kwargs):
        # Check if the user associated with the business is a seller
        if self.user.role != 'seller':
            raise ValueError("Only users with the role 'seller' can register a business.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='category_images/')
    name = models.CharField(max_length=255)
       
    def __str__(self):
        return self.name
    
class Product(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sold = models.PositiveIntegerField(default=0) 
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name

    def view(self):
        return f'/products/{self.id}/'

    def edit(self):
        return f'/products/{self.id}/edit/'

    def delete(self):
        return f'/products/{self.id}/delete/'

