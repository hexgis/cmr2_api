from django.contrib import admin
from land_use_mapping import models


class LandUseMappingClassesAdmin(admin.ModelAdmin):
    # list_display = '__all__'

    # fields = list_display

    # search_fields = list_display
    pass


class LandUseMappingTIAdmin(admin.ModelAdmin):
    # list_display = '__all__'

    # fields = list_display

    # search_fields = list_display
    pass


admin.site.register(models.LandUseMappingClasses, LandUseMappingClassesAdmin)
admin.site.register(models.LandUseMappingTI, LandUseMappingTIAdmin)
