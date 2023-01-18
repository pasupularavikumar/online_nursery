
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name=models.CharField(max_length=150)
    price=models.FloatField()
    Description=models.TextField()
    choices=(('Indoor Plant','indoor plant'),('Native plant','native plant'),('Pots','pots'),('Fertilizer','fertilizer'))
    image=models.ImageField()
    categories=models.CharField(max_length=200,choices=choices)
    relatedproduct=models.ManyToManyField('self',blank=True,null=True)
    def __str__(self):
        return self.name
    
class cartObject(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    products=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()

class cart(models.Model):
    cartObject=models.ManyToManyField(cartObject)
    def __str__(self):
        return self.user.username
    
class placedOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    address = models.CharField(max_length=254, null=True, blank=True)
    phone = models.CharField(max_length=254, null=True, blank=True)
    paymentObject = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.user.username
#--class RecommendedProducts(models.Model):
   # mainproduct=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='mainproduct')
    #relatedproduct=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='relatedproduct')

    

    
    
