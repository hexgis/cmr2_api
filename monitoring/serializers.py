from utils.format_values import format_area, format_coord, format_date, format_percentage
from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers
from monitoring import models
# Configura a localidade para o formato brasileiro


class MonitoringConsolidatedSerializer(gis_serializers.GeoFeatureModelSerializer):
    """Serializer for `models.MonitoringConsolidated` data."""
    nu_area_ha = serializers.SerializerMethodField()
    nu_latitude = serializers.SerializerMethodField()
    nu_longitude = serializers.SerializerMethodField()
    dt_imagem = serializers.SerializerMethodField()
    dt_t_zero = serializers.SerializerMethodField()
    dt_t_um = serializers.SerializerMethodField()

    class Meta:
        """Meta class for `MonitoringConsolidatedSerializer` serializer."""
        model = models.MonitoringConsolidated
        geo_field = 'geom'
        id_field = False
        fields = (
            'id',
            'no_imagem',
            'dt_imagem',
            'no_estagio',
            'nu_orbita',
            'nu_ponto',
            'nu_latitude',
            'nu_longitude',
            'dt_t_zero',
            'dt_t_um',
            'co_funai',
            'nu_area_km2',
            'nu_area_ha',
            'co_cr',
            'ds_cr',
            'no_ti',
            'ti_nu_area_ha',
            'geom',
        )

    def get_nu_area_ha(self, obj):
        return format_area(obj.nu_area_ha)

    def get_nu_latitude(self, obj):
        return format_coord(obj.nu_latitude)

    def get_nu_longitude(self, obj):
        return format_coord(obj.nu_longitude)

    def get_dt_imagem(self, obj):
        return format_date(obj.dt_imagem)

    def get_dt_t_zero(self, obj):
        return format_date(obj.dt_t_zero)

    def get_dt_t_um(self, obj):
        return format_date(obj.dt_t_um)


class MonitoringConsolidatedDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed `models.MonitoringConsolidated` data."""
    nu_area_ha = serializers.SerializerMethodField()
    nu_latitude = serializers.SerializerMethodField()
    nu_longitude = serializers.SerializerMethodField()
    dt_t_zero = serializers.SerializerMethodField()
    dt_t_um = serializers.SerializerMethodField()
    ti_nu_area_ha = serializers.SerializerMethodField()

    class Meta:
        """Meta class for `MonitoringConsolidatedDetailSerializer` serializer."""
        model = models.MonitoringConsolidated
        id_field = False
        fields = (
            'co_funai',
            'no_ti',
            'ds_cr',
            'no_estagio',
            'no_imagem',
            'dt_t_zero',
            'dt_t_um',
            'nu_area_ha',
            'nu_latitude',
            'nu_longitude',
            'ti_nu_area_ha',
        )

    def get_nu_area_ha(self, obj):
        return format_area(obj.nu_area_ha)

    def get_nu_latitude(self, obj):
        return format_coord(obj.nu_latitude)

    def get_nu_longitude(self, obj):
        return format_coord(obj.nu_longitude)

    def get_dt_t_zero(self, obj):
        return format_date(obj.dt_t_zero)

    def get_dt_t_um(self, obj):
        return format_date(obj.dt_t_um)

    def get_ti_nu_area_ha(self, obj):
        return format_area(obj.ti_nu_area_ha)


class MonitoringConsolidatedClassesSerializer(serializers.ModelSerializer):
    """Serializer for stages 'models.MonitoringConsolidated' data."""

    class Meta:
        """Meta class for `MonitoringConsolidatedClassesSerializer` serializer."""
        model = models.MonitoringConsolidated
        id_field = False
        fields = ('no_estagio',)


class MonitoringConsolidatedTableSerializer(serializers.ModelSerializer):
    """Serializer for table 'models.MonitoringConsolidated' data."""
    nu_area_ha = serializers.SerializerMethodField()
    nu_latitude = serializers.SerializerMethodField()
    nu_longitude = serializers.SerializerMethodField()
    dt_imagem = serializers.SerializerMethodField()
    dt_t_zero = serializers.SerializerMethodField()
    dt_t_um = serializers.SerializerMethodField()
    ti_nu_area_ha = serializers.SerializerMethodField()

    class Meta:
        """Meta class for `MonitoringConsolidatedTableSerializer` serializer."""
        model = models.MonitoringConsolidated
        id_field = False
        fields = (
            'id',
            'no_imagem',
            'dt_imagem',
            'no_estagio',
            'nu_orbita',
            'nu_ponto',
            'nu_latitude',
            'nu_longitude',
            'dt_t_zero',
            'dt_t_um',
            'co_funai',
            'nu_area_km2',
            'nu_area_ha',
            'co_cr',
            'ds_cr',
            'no_ti',
            'ti_nu_area_ha',
        )

    def get_nu_area_ha(self, obj):
        return format_area(obj.nu_area_ha)

    def get_nu_latitude(self, obj):
        return format_coord(obj.nu_latitude)

    def get_nu_longitude(self, obj):
        return format_coord(obj.nu_longitude)

    def get_dt_imagem(self, obj):
        return format_date(obj.dt_imagem)

    def get_dt_t_zero(self, obj):
        return format_date(obj.dt_t_zero)

    def get_dt_t_um(self, obj):
        return format_date(obj.dt_t_um)

    def get_ti_nu_area_ha(self, obj):
        return format_area(obj.ti_nu_area_ha)


class MonitoringConsolidatedByCoFunaiAndYearSerializer(serializers.ModelSerializer):
    """Serializer for table `models.MonitoringConsolidated` data."""
    ano = serializers.IntegerField()
    cr_nu_area_ha = serializers.SerializerMethodField()
    dg_nu_area_ha = serializers.SerializerMethodField()
    dr_nu_area_ha = serializers.SerializerMethodField()
    ff_nu_area_ha = serializers.SerializerMethodField()
    total_nu_area_ha = serializers.SerializerMethodField()
    ti_nu_area_ha = serializers.SerializerMethodField()
    cr_nu_area_perc = serializers.SerializerMethodField()
    dg_nu_area_perc = serializers.SerializerMethodField()
    dr_nu_area_perc = serializers.SerializerMethodField()
    ff_nu_area_perc = serializers.SerializerMethodField()

    class Meta:
        """Meta class for `MonitoringConsolidatedByCoFunaiAndYearSerializer` serializer."""
        model = models.MonitoringConsolidated
        fields = [
            'ano',
            'co_funai',
            'no_ti',
            'ti_nu_area_ha',
            'cr_nu_area_ha',
            'dg_nu_area_ha',
            'dr_nu_area_ha',
            'ff_nu_area_ha',
            'cr_nu_area_perc',
            'dg_nu_area_perc',
            'dr_nu_area_perc',
            'ff_nu_area_perc',
            'total_nu_area_ha'
        ]

    def get_cr_nu_area_ha(self, obj):
        return format_area(obj.get('cr_nu_area_ha'))

    def get_dg_nu_area_ha(self, obj):
        return format_area(obj.get('dg_nu_area_ha'))

    def get_dr_nu_area_ha(self, obj):
        return format_area(obj.get('dr_nu_area_ha'))

    def get_ff_nu_area_ha(self, obj):
        return format_area(obj.get('ff_nu_area_ha'))

    def get_total_nu_area_ha(self, obj):
        return format_area(obj.get('total_nu_area_ha'))

    def get_ti_nu_area_ha(self, obj):
        return format_area(obj.get('ti_nu_area_ha'))

    def get_cr_nu_area_perc(self, obj):
        return format_percentage(obj.get('cr_nu_area_perc'))

    def get_dg_nu_area_perc(self, obj):
        return format_percentage(obj.get('dg_nu_area_perc'))

    def get_dr_nu_area_perc(self, obj):
        return format_percentage(obj.get('dr_nu_area_perc'))

    def get_ff_nu_area_perc(self, obj):
        return format_percentage(obj.get('ff_nu_area_perc'))


class MonitoringConsolidatedByCoFunaiAndMonthYearSerializer(serializers.ModelSerializer):
    """Serializer for table `models.MonitoringConsolidated` data."""
    mes = serializers.IntegerField()
    ano = serializers.IntegerField()
    cr_nu_area_ha = serializers.SerializerMethodField()
    dg_nu_area_ha = serializers.SerializerMethodField()
    dr_nu_area_ha = serializers.SerializerMethodField()
    ff_nu_area_ha = serializers.SerializerMethodField()
    total_nu_area_ha = serializers.SerializerMethodField()
    ti_nu_area_ha = serializers.SerializerMethodField()
    cr_nu_area_perc = serializers.SerializerMethodField()
    dg_nu_area_perc = serializers.SerializerMethodField()
    dr_nu_area_perc = serializers.SerializerMethodField()
    ff_nu_area_perc = serializers.SerializerMethodField()

    class Meta:
        """Meta class for `MonitoringConsolidatedByCoFunaiAndMonthYearSerializer` serializer."""
        model = models.MonitoringConsolidated
        fields = [
            'ano',
            'mes',
            'co_funai',
            'no_ti',
            'ti_nu_area_ha',
            'cr_nu_area_ha',
            'dg_nu_area_ha',
            'dr_nu_area_ha',
            'ff_nu_area_ha',
            'cr_nu_area_perc',
            'dg_nu_area_perc',
            'dr_nu_area_perc',
            'ff_nu_area_perc',
            'total_nu_area_ha'
        ]

    def get_cr_nu_area_ha(self, obj):
        return format_area(obj.get('cr_nu_area_ha'))

    def get_dg_nu_area_ha(self, obj):
        return format_area(obj.get('dg_nu_area_ha'))

    def get_dr_nu_area_ha(self, obj):
        return format_area(obj.get('dr_nu_area_ha'))

    def get_ff_nu_area_ha(self, obj):
        return format_area(obj.get('ff_nu_area_ha'))

    def get_total_nu_area_ha(self, obj):
        return format_area(obj.get('total_nu_area_ha'))

    def get_ti_nu_area_ha(self, obj):
        return format_area(obj.get('ti_nu_area_ha'))

    def get_cr_nu_area_perc(self, obj):
        return format_percentage(obj.get('cr_nu_area_perc'))

    def get_dg_nu_area_perc(self, obj):
        return format_percentage(obj.get('dg_nu_area_perc'))

    def get_dr_nu_area_perc(self, obj):
        return format_percentage(obj.get('dr_nu_area_perc'))

    def get_ff_nu_area_perc(self, obj):
        return format_percentage(obj.get('ff_nu_area_perc'))


class MonitoringConsolidatedByCoFunaiSerializer(serializers.ModelSerializer):
    """Serializer for table `models.MonitoringConsolidated` data."""
    cr_nu_area_ha = serializers.SerializerMethodField()
    dg_nu_area_ha = serializers.SerializerMethodField()
    dr_nu_area_ha = serializers.SerializerMethodField()
    ff_nu_area_ha = serializers.SerializerMethodField()
    total_nu_area_ha = serializers.SerializerMethodField()
    ti_nu_area_ha = serializers.SerializerMethodField()
    cr_nu_area_perc = serializers.SerializerMethodField()
    dg_nu_area_perc = serializers.SerializerMethodField()
    dr_nu_area_perc = serializers.SerializerMethodField()
    ff_nu_area_perc = serializers.SerializerMethodField()

    class Meta:
        """Meta class for `MonitoringConsolidatedByCoFunaiSerializer` serializer."""
        model = models.MonitoringConsolidated
        fields = [
            'co_funai',
            'no_ti',
            'ti_nu_area_ha',
            'cr_nu_area_ha',
            'dg_nu_area_ha',
            'dr_nu_area_ha',
            'ff_nu_area_ha',
            'cr_nu_area_perc',
            'dg_nu_area_perc',
            'dr_nu_area_perc',
            'ff_nu_area_perc',
            'total_nu_area_ha'
        ]

    def get_cr_nu_area_ha(self, obj):
        return format_area(obj.get('cr_nu_area_ha'))

    def get_dg_nu_area_ha(self, obj):
        return format_area(obj.get('dg_nu_area_ha'))

    def get_dr_nu_area_ha(self, obj):
        return format_area(obj.get('dr_nu_area_ha'))

    def get_ff_nu_area_ha(self, obj):
        return format_area(obj.get('ff_nu_area_ha'))

    def get_total_nu_area_ha(self, obj):
        return format_area(obj.get('total_nu_area_ha'))

    def get_ti_nu_area_ha(self, obj):
        return format_area(obj.get('ti_nu_area_ha'))

    def get_cr_nu_area_perc(self, obj):
        return format_percentage(obj.get('cr_nu_area_perc'))

    def get_dg_nu_area_perc(self, obj):
        return format_percentage(obj.get('dg_nu_area_perc'))

    def get_dr_nu_area_perc(self, obj):
        return format_percentage(obj.get('dr_nu_area_perc'))

    def get_ff_nu_area_perc(self, obj):
        return format_percentage(obj.get('ff_nu_area_perc'))


class MonitoringConsolidatedByMonthYearSerializer(serializers.ModelSerializer):
    """Serializer for table `models.MonitoringConsolidated` data."""
    mes = serializers.IntegerField()
    ano = serializers.IntegerField()
    cr_nu_area_ha = serializers.SerializerMethodField()
    dg_nu_area_ha = serializers.SerializerMethodField()
    dr_nu_area_ha = serializers.SerializerMethodField()
    ff_nu_area_ha = serializers.SerializerMethodField()
    total_nu_area_ha = serializers.SerializerMethodField()

    class Meta:
        """Metaclass for `MonitoringConsolidatedByMonthYearSerializer` serializer."""
        model = models.MonitoringConsolidated
        fields = [
            'ano',
            'mes',
            'cr_nu_area_ha',
            'dg_nu_area_ha',
            'dr_nu_area_ha',
            'ff_nu_area_ha',
            'total_nu_area_ha'
        ]

    def get_cr_nu_area_ha(self, obj):
        return format_area(obj.get('cr_nu_area_ha'))

    def get_dg_nu_area_ha(self, obj):
        return format_area(obj.get('dg_nu_area_ha'))

    def get_dr_nu_area_ha(self, obj):
        return format_area(obj.get('dr_nu_area_ha'))

    def get_ff_nu_area_ha(self, obj):
        return format_area(obj.get('ff_nu_area_ha'))

    def get_total_nu_area_ha(self, obj):
        return format_area(obj.get('total_nu_area_ha'))


class MonitoringConsolidatedByYearSerializer(serializers.ModelSerializer):
    """Serializer for table `models.MonitoringConsolidated` data."""
    ano = serializers.IntegerField()
    cr_nu_area_ha = serializers.SerializerMethodField()
    dg_nu_area_ha = serializers.SerializerMethodField()
    dr_nu_area_ha = serializers.SerializerMethodField()
    ff_nu_area_ha = serializers.SerializerMethodField()
    total_nu_area_ha = serializers.SerializerMethodField()

    class Meta:
        """Meta class for `MonitoringConsolidatedByYearSerializer` serializer."""
        model = models.MonitoringConsolidated
        fields = [
            'ano',
            'cr_nu_area_ha',
            'dg_nu_area_ha',
            'dr_nu_area_ha',
            'ff_nu_area_ha',
            'total_nu_area_ha'
        ]

    def get_cr_nu_area_ha(self, obj):
        return format_area(obj.get('cr_nu_area_ha'))

    def get_dg_nu_area_ha(self, obj):
        return format_area(obj.get('dg_nu_area_ha'))

    def get_dr_nu_area_ha(self, obj):
        return format_area(obj.get('dr_nu_area_ha'))

    def get_ff_nu_area_ha(self, obj):
        return format_area(obj.get('ff_nu_area_ha'))

    def get_total_nu_area_ha(self, obj):
        return format_area(obj.get('total_nu_area_ha'))


class MonitoringConsolidatedByDaySerializer(serializers.ModelSerializer):
    """Serializer for table `models.MonitoringConsolidated` data."""
    cr_nu_area_ha = serializers.SerializerMethodField()
    dg_nu_area_ha = serializers.SerializerMethodField()
    dr_nu_area_ha = serializers.SerializerMethodField()
    ff_nu_area_ha = serializers.SerializerMethodField()
    total_nu_area_ha = serializers.SerializerMethodField()
    ti_nu_area_ha = serializers.SerializerMethodField()
    dt_t_um = serializers.SerializerMethodField()

    class Meta:
        """Meta class for `MonitoringConsolidatedByDaySerializer` serializer."""
        model = models.MonitoringConsolidated
        fields = [
            'co_funai',
            'no_ti',
            'dt_t_um',
            'ti_nu_area_ha',
            'cr_nu_area_ha',
            'dg_nu_area_ha',
            'dr_nu_area_ha',
            'ff_nu_area_ha',
            'total_nu_area_ha'
        ]

    def get_cr_nu_area_ha(self, obj):
        return format_area(obj.get('cr_nu_area_ha'))

    def get_dg_nu_area_ha(self, obj):
        return format_area(obj.get('dg_nu_area_ha'))

    def get_dr_nu_area_ha(self, obj):
        return format_area(obj.get('dr_nu_area_ha'))

    def get_ff_nu_area_ha(self, obj):
        return format_area(obj.get('ff_nu_area_ha'))

    def get_total_nu_area_ha(self, obj):
        return format_area(obj.get('total_nu_area_ha'))

    def get_ti_nu_area_ha(self, obj):
        return format_area(obj.get('ti_nu_area_ha'))

    def get_dt_t_um(self, obj):
        return format_date(obj.get('dt_t_um'))
