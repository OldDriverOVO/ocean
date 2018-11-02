from django.contrib import admin
from .models import Parts,Factory,FactoryPartsPrice,Customer,CustomerPartsPrice,VolumeWeightData,OemExchange
# Register your models here.
admin.site.register(Parts)
admin.site.register(Factory)
admin.site.register(FactoryPartsPrice)
admin.site.register(Customer)
admin.site.register(CustomerPartsPrice)
admin.site.register(VolumeWeightData)
admin.site.register(OemExchange)
