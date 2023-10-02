from django.contrib import admin
from .models import (ContinentConsumption, CountryConsumption,
                     NonRenewablesTotalPowerGenerated,
                     RenewablesPowerGenerated, RenewableTotalPowerGenerated,
                     TopTwentyRenewableCountries)


class CountryConsumptionAdmin(admin.ModelAdmin):
    ordering = ['year']


# Register your models here.
admin.site.register(ContinentConsumption)
admin.site.register(CountryConsumption, CountryConsumptionAdmin)
admin.site.register(NonRenewablesTotalPowerGenerated)
admin.site.register(RenewablesPowerGenerated)
admin.site.register(RenewableTotalPowerGenerated)
admin.site.register(TopTwentyRenewableCountries)
