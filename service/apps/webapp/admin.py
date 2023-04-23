from django.contrib import admin

from apps.webapp.models import ManagerDownload, Banner, Country, ChinaProvinceArea

admin.site.register(ManagerDownload)
admin.site.register(Banner)
admin.site.register(Country)
admin.site.register(ChinaProvinceArea)
