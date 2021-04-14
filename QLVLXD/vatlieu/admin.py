from django.contrib import admin

# Register your models here.
from .models import *

# add data to admin to control

admin.site.register(Customer)
admin.site.register(Provider)
admin.site.register(TypeProduct)
admin.site.register(Calculation_Unit)
admin.site.register(Product)
admin.site.register(Warehouse)
admin.site.register(InputBill)
admin.site.register(DetailInputBill)
admin.site.register(OutputBill)
admin.site.register(DetailOutputBill)
admin.site.register(Shopping)