from django.contrib import admin
from land_use import models


class LandUseClassesAdmin(admin.ModelAdmin):
    # list_display = '__all__'

    # fields = list_display

    # search_fields = list_display
    pass


class LandUseTIAdmin(admin.ModelAdmin):
    # list_display = '__all__'

    # fields = list_display

    # search_fields = list_display
    pass


admin.site.register(models.LandUseClasses, LandUseClassesAdmin)
admin.site.register(models.LandUseTI, LandUseTIAdmin)
