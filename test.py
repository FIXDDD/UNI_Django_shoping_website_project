import datetime
from test001.models import *


# To add Item to product table
def add_item():
    obj = Products.objects.create(
        Product_ID=3,
        Product_type='Adventure',
        Product_name='Harry Potter and the Chamber of Secrets',
        Product_price=1.70,
        DisplayImage='image/Harry-Potter-and-the-Chamber-of-Secrets.jpg',
        Brand='Bloomsbury',
        ISBN=9780747538486,
        Authors='Rowling, J. K.',
        Publisher= 'London',
        Num_of_pages=600,
        Description='asdfdasfsadfasfdafafwefsdfgsdfga',
        Release_date=datetime.date(1999, 10, 4)
    )
    obj.save()

# https://blog.csdn.net/qq_19691995/article/details/102961465
# Date cant be change manually in db Datefield , need to be change by code using 'python console'
#  To change the date of exist data, change the date and POnumber bellow\
#  In python console insert:
#   from test import *
#   change_date()
#
def change_date():
    time = datetime.datetime(2020, 2, 21, 6, 00, 00)
    print(time)
    obj = Order.objects.filter(POnumber=5).update(Order_date=time)
    print(obj)


