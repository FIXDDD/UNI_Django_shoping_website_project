from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

"""
~ Integer Field ignore max_length parameter, validator is implemented to for length value restrictions
  validators will not run automatically when you save a model, but if you are using a ModelForm,
  it will run your validators on the fields that are included in the form.

~ Django model do not support two primary key, use unique together for unique restrictions.
  However Django will add an auto increment id field to table which don't specific primary key = true
  
~ Extent Django auth_user to customer to user Django uer authorization functions
  Method link:
  https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
  

"""


# Create your models here.

# Store products information
class Products(models.Model):
    Product_ID = models.IntegerField(primary_key=True)  # Generate by code
    Product_type = models.TextField()
    Product_name = models.TextField()
    Product_price = models.DecimalField(max_digits=30, decimal_places=2)  # Define as decimal in dictionary/ Double
    DisplayImage = models.CharField(max_length=255)  # Enough?
    Brand = models.TextField()
    ISBN = models.IntegerField(validators=[MaxValueValidator(9999999999999)])
    Authors = models.CharField(max_length=255)
    Publisher = models.CharField(max_length=255)
    Release_date = models.DateField()
    Num_of_pages = models.IntegerField(validators=[MaxValueValidator(9999999999)])
    Description = models.TextField()

    class Meta:
        db_table = 'Products'


# Store all image of each product
class DetailImage(models.Model):
    Product_ID = models.ForeignKey(Products, on_delete=models.CASCADE)  # Generate by code
    Img_ID = models.IntegerField(validators=[MaxValueValidator(9)])  # max length = 1? / generate by code?
    Img_URL = models.CharField(max_length=255)  # Define as text in dictionary / Recommend to store url in varchar

    class Meta:
        db_table = 'DetailImage'
        unique_together = (("Product_ID", "Img_ID"),)  # PK


# Store Customer Information
# Extends form auth_user table
class Customer(models.Model):
    Cust_iD = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    Address = models.CharField(max_length=255)

    class Meta:
        db_table = 'Customer'


# Hookup User and Customer table for auto create when new user created
@receiver(post_save, sender=User)
def create_user_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(Cust_iD=instance)


@receiver(post_save, sender=User)
def save_user_customer(sender, instance, **kwargs):
    instance.customer.save()


# Store Customer purchase item list
class Shopping_cart(models.Model):
    Cust_ID = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Product_ID = models.ForeignKey(Products, on_delete=models.CASCADE)
    Quantity = models.IntegerField(validators=[MaxValueValidator(99999)])

    class Meta:
        db_table = 'Shopping_cart'
        unique_together = (("Cust_ID", "Product_ID"),)  # PK


# Store Purchase Order item
class Order(models.Model):
    POnumber = models.IntegerField(primary_key=True)  # Generate by code /
    Cust_ID = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Order_date = models.DateTimeField(null=True)
    Cancel_date = models.DateField(null=True)
    Ship_date = models.DateField(null=True)
    Status = models.TextField()
    Total_payment = models.DecimalField(max_digits=30, decimal_places=2)  # Define as decimal in dictionary / Double
    Cancel_by = models.CharField(null=True, max_length=10)

    class Meta:
        db_table = 'Order'


# Store product customer purchase per order
class Order_Items(models.Model):
    POnumber = models.ForeignKey(Order, on_delete=models.CASCADE)
    Product_ID = models.ForeignKey(Products, on_delete=models.CASCADE)
    Product_price = models.DecimalField(max_digits=30, decimal_places=2)  # Define as decimal in dictionary / Double
    Quantity = models.IntegerField(validators=[MaxValueValidator(99999)])

    class Meta:
        db_table = 'Order_Items'
        unique_together = (("POnumber", "Product_ID"),)  # PK
