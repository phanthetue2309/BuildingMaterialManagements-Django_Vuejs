from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime    
from django.utils.translation import gettext as _ # using in datetime
# Create your models here.


class AbstractPerson(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    address = models.CharField(max_length=45, null=True)
    phone_number = models.CharField(max_length=45, null=True)
    discription = models.TextField(null=True)

    def __str__(self):  # show the name of customer when print
        return self.name

    class Meta:
        abstract = True


class Customer(AbstractPerson):
    pass

    

class Provider(AbstractPerson):
    pass



class TypeProduct(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=255)
    flag = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class Calculation_Unit(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    type_product = models.ForeignKey(TypeProduct, on_delete=models.CASCADE, related_name="products")
    calculationUnit = models.ForeignKey(Calculation_Unit, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=45)
    unit_cost = models.IntegerField(default=10000)
    selling_price = models.IntegerField(default=10000, null=True)
    origin = models.CharField(max_length=45)  # xuất xứ

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('list-product')

    class Meta:
        ordering = ['type_product__name']


class Warehouse(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="warehouses", blank=True,
                                null=True)
    count = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return str(self.product.name)

    class Meta:
        ordering = ['product__type_product__name']

# input
class Bill(models.Model) :
    STATUS = (
        (1, 'Pending'),
        (0, 'Out for delivery'),
        (-1, 'Delivered'),
    )
    id = models.AutoField(primary_key=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    flag = models.IntegerField(default=1, choices=STATUS)

    class Meta:
        abstract = True


class InputBill(Bill):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name="input_bills")
    input_date = models.DateField(_("Date"), default=datetime.today)

    def __str__(self):
        return str(self.provider)

    def get_absolute_url(self):
        return reverse('input-bill-detail-create', kwargs={'pk': self.pk})


class DetailInputBill(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    input_bill = models.ForeignKey(InputBill, null=True, on_delete=models.SET_NULL)
    count = models.IntegerField(default=1)
    price = models.IntegerField(default=10000)

    def __str__(self):
        return str(self.product.name)

    def get_absolute_url(self):
        return reverse('input-bill-detail-create', kwargs={'pk': self.pk})

    def get_update_return(self):
        return reverse('input-bill-detail', kwargs={'pk': self.input_bill.pk})


# output
class OutputBill(Bill):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="output_bills")
    output_date = models.DateField(_("Date"), default=datetime.today)

    def __str__(self):
        return str(self.customer)

    def get_absolute_url(self):
        return reverse('output-bill-detail-create', kwargs={'pk': self.pk})


class DetailOutputBill(models.Model):
    id = models.AutoField(primary_key=True)
    warehouse = models.ForeignKey(Warehouse, null=True, on_delete=models.SET_NULL)
    output_bill = models.ForeignKey(OutputBill, null=True, on_delete=models.SET_NULL)
    count = models.IntegerField(default=1)
    price = models.IntegerField(default=10000)

    def __str__(self):
        return str(self.warehouse.product.name)

    def get_absolute_url(self):
        return reverse('output-bill-detail-create', kwargs={'pk': self.pk})

    def get_update_return(self):
        return reverse('output-bill-detail', kwargs={'pk': self.output_bill.pk})


class Shopping(Bill):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    buy_date = models.DateTimeField(default=datetime.now, blank=True)
    count = models.IntegerField(default=1)
    total_cost = models.IntegerField(default=0, null=True)
    buying_unit_cost = models.IntegerField(default=10000, null=True)

    def __str__(self):
        return str(self.product.name)