from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers
from django.utils.formats import number_format
from monitoring import models

import locale

try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
    except locale.Error:
        locale.setlocale(locale.LC_ALL, 'pt_BR')


class MonitoringConsolidatedSerializer(
    gis_serializers.GeoFeatureModelSerializer
):
    """Serializer for `models.MonitoringConsolidated` data."""

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


class MonitoringConsolidatedDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed `models.MonitoringConsolidated` data."""

    class Meta:
        """
        Meta class for `MonitoringConsolidatedDetailSerializer` serializer.
        """
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


def to_representation(instance) -> str:
    """Representates model data instance as simple string.

    Returns:
        str: abbreviation of types stages
    """
    return f'{instance.no_estagio}'


class MonitoringConsolidatedClassesSerializer(serializers.ModelSerializer):
    """Serializer for stages 'models.MonitoringConsolidated' data."""

    class Meta:
        """
        Meta class for `MonitoringConsolidatedClassesSerializer` serializer.
        """
        model = models.MonitoringConsolidated
        id_field = False
        fields = ('no_estagio',)


class MonitoringConsolidatedTableSerializer(
    serializers.ModelSerializer
):
    """Serializer for table 'models.MonitoringConsolidated' data."""

    class Meta:
        """Meta class for
        `MonitoringConsolidatedTableSerializer` serializer."""
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


class MonitoringConsolidatedByCoFunaiAndYearSerializer(
    serializers.ModelSerializer
):
    """Serializer for table `models.MonitoringConsolidated` data."""

    ano = serializers.IntegerField()

    # Campos de área (com milhares e decimais personalizados)
    cr_nu_area_ha = serializers.SerializerMethodField()
    dg_nu_area_ha = serializers.SerializerMethodField()
    dr_nu_area_ha = serializers.SerializerMethodField()
    ff_nu_area_ha = serializers.SerializerMethodField()
    total_nu_area_ha = serializers.SerializerMethodField()
    ti_nu_area_ha = serializers.SerializerMethodField()

    # Campos percentuais (com 6 decimais e símbolo de %)
    cr_nu_area_perc = serializers.SerializerMethodField()
    dg_nu_area_perc = serializers.SerializerMethodField()
    dr_nu_area_perc = serializers.SerializerMethodField()
    ff_nu_area_perc = serializers.SerializerMethodField()

    class Meta:
        """Meta class for
        `MonitoringConsolidatedByCoFunaiAndYearSerializer` serializer."""
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

    # Métodos para formatação de campos de área
    def format_area(self, value):
        return locale.format_string("%.3f", value, grouping=True)

    def get_cr_nu_area_ha(self, obj):
        return self.format_area(obj['cr_nu_area_ha'])

    def get_dg_nu_area_ha(self, obj):
        return self.format_area(obj['dg_nu_area_ha'])

    def get_dr_nu_area_ha(self, obj):
        return self.format_area(obj['dr_nu_area_ha'])

    def get_ff_nu_area_ha(self, obj):
        return self.format_area(obj['ff_nu_area_ha'])

    def get_total_nu_area_ha(self, obj):
        return self.format_area(obj['total_nu_area_ha'])

    def get_ti_nu_area_ha(self, obj):
        return self.format_area(obj['ti_nu_area_ha'])

    def format_percentage(self, value):
        formatted_value = number_format(
            value,
            decimal_pos=6,
            use_l10n=True,
            force_grouping=True
        )
        return f"{formatted_value}%"

    def get_cr_nu_area_perc(self, obj):
        return self.format_percentage(obj['cr_nu_area_perc'])

    def get_dg_nu_area_perc(self, obj):
        return self.format_percentage(obj['dg_nu_area_perc'])

    def get_dr_nu_area_perc(self, obj):
        return self.format_percentage(obj['dr_nu_area_perc'])

    def get_ff_nu_area_perc(self, obj):
        return self.format_percentage(obj['ff_nu_area_perc'])


class MonitoringConsolidatedByCoFunaiAndMonthYearSerializer(
    serializers.ModelSerializer
):
    """Serializer for table `models.MonitoringConsolidated` data."""
    mes = serializers.IntegerField()
    ano = serializers.IntegerField()

    # Campos de área (com milhares e decimais personalizados)
    cr_nu_area_ha = serializers.SerializerMethodField()
    dg_nu_area_ha = serializers.SerializerMethodField()
    dr_nu_area_ha = serializers.SerializerMethodField()
    ff_nu_area_ha = serializers.SerializerMethodField()
    total_nu_area_ha = serializers.SerializerMethodField()
    ti_nu_area_ha = serializers.SerializerMethodField()

    # Campos percentuais (com 6 decimais e símbolo de %)
    cr_nu_area_perc = serializers.SerializerMethodField()
    dg_nu_area_perc = serializers.SerializerMethodField()
    dr_nu_area_perc = serializers.SerializerMethodField()
    ff_nu_area_perc = serializers.SerializerMethodField()

    class Meta:
        """Meta class for
        `MonitoringConsolidatedByCoFunaiAndMonthYearSerializer` serializer."""
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

    # Métodos para formatação de campos de área
    def format_area(self, value):
        return locale.format_string("%.3f", value, grouping=True)

    def get_cr_nu_area_ha(self, obj):
        return self.format_area(obj['cr_nu_area_ha'])

    def get_dg_nu_area_ha(self, obj):
        return self.format_area(obj['dg_nu_area_ha'])

    def get_dr_nu_area_ha(self, obj):
        return self.format_area(obj['dr_nu_area_ha'])

    def get_ff_nu_area_ha(self, obj):
        return self.format_area(obj['ff_nu_area_ha'])

    def get_total_nu_area_ha(self, obj):
        return self.format_area(obj['total_nu_area_ha'])

    def get_ti_nu_area_ha(self, obj):
        return self.format_area(obj['ti_nu_area_ha'])

    # Métodos para formatação de campos percentuais
    def format_percentage(self, value):
        return f"{value:.6f}%"

    def get_cr_nu_area_perc(self, obj):
        return self.format_percentage(obj['cr_nu_area_perc'])

    def get_dg_nu_area_perc(self, obj):
        return self.format_percentage(obj['dg_nu_area_perc'])

    def get_dr_nu_area_perc(self, obj):
        return self.format_percentage(obj['dr_nu_area_perc'])

    def get_ff_nu_area_perc(self, obj):
        return self.format_percentage(obj['ff_nu_area_perc'])


class MonitoringConsolidatedByCoFunaiSerializer(serializers.ModelSerializer):
    """Serializer for table `models.MonitoringConsolidated` data."""
    # Campos de área (com milhares e decimais personalizados)
    cr_nu_area_ha = serializers.SerializerMethodField()
    dg_nu_area_ha = serializers.SerializerMethodField()
    dr_nu_area_ha = serializers.SerializerMethodField()
    ff_nu_area_ha = serializers.SerializerMethodField()
    total_nu_area_ha = serializers.SerializerMethodField()
    ti_nu_area_ha = serializers.SerializerMethodField()

    # Campos percentuais (com 6 decimais e símbolo de %)
    cr_nu_area_perc = serializers.SerializerMethodField()
    dg_nu_area_perc = serializers.SerializerMethodField()
    dr_nu_area_perc = serializers.SerializerMethodField()
    ff_nu_area_perc = serializers.SerializerMethodField()

    class Meta:
        """Meta class for `MonitoringConsolidatedByCoFunaiSerializer`
        serializer."""
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

    # Métodos para formatação de campos de área
    def format_area(self, value):
        return locale.format_string("%.3f", value, grouping=True)

    def get_cr_nu_area_ha(self, obj):
        return self.format_area(obj['cr_nu_area_ha'])

    def get_dg_nu_area_ha(self, obj):
        return self.format_area(obj['dg_nu_area_ha'])

    def get_dr_nu_area_ha(self, obj):
        return self.format_area(obj['dr_nu_area_ha'])

    def get_ff_nu_area_ha(self, obj):
        return self.format_area(obj['ff_nu_area_ha'])

    def get_total_nu_area_ha(self, obj):
        return self.format_area(obj['total_nu_area_ha'])

    def get_ti_nu_area_ha(self, obj):
        return self.format_area(obj['ti_nu_area_ha'])

    # Métodos para formatação de campos percentuais
    def format_percentage(self, value):
        return f"{value:.6f}%"

    def get_cr_nu_area_perc(self, obj):
        return self.format_percentage(obj['cr_nu_area_perc'])

    def get_dg_nu_area_perc(self, obj):
        return self.format_percentage(obj['dg_nu_area_perc'])

    def get_dr_nu_area_perc(self, obj):
        return self.format_percentage(obj['dr_nu_area_perc'])

    def get_ff_nu_area_perc(self, obj):
        return self.format_percentage(obj['ff_nu_area_perc'])


class MonitoringConsolidatedByMonthYearSerializer(
    serializers.ModelSerializer
):
    """Serializer for table `models.MonitoringConsolidated` data."""

    mes = serializers.IntegerField()
    ano = serializers.IntegerField()

    # Campos de área (com milhares e decimais personalizados)
    cr_nu_area_ha = serializers.SerializerMethodField()
    dg_nu_area_ha = serializers.SerializerMethodField()
    dr_nu_area_ha = serializers.SerializerMethodField()
    ff_nu_area_ha = serializers.SerializerMethodField()
    total_nu_area_ha = serializers.SerializerMethodField()

    class Meta:
        """Metaclass for
        `MonitoringConsolidatedByMonthYearSerializer` serializer."""
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

    # Métodos para formatação de campos de área
    def format_area(self, value):
        return locale.format_string("%.3f", value, grouping=True)

    def get_cr_nu_area_ha(self, obj):
        return self.format_area(obj['cr_nu_area_ha'])

    def get_dg_nu_area_ha(self, obj):
        return self.format_area(obj['dg_nu_area_ha'])

    def get_dr_nu_area_ha(self, obj):
        return self.format_area(obj['dr_nu_area_ha'])

    def get_ff_nu_area_ha(self, obj):
        return self.format_area(obj['ff_nu_area_ha'])

    def get_total_nu_area_ha(self, obj):
        return self.format_area(obj['total_nu_area_ha'])


class MonitoringConsolidatedByYearSerializer(serializers.ModelSerializer):
    """Serializer for table `models.MonitoringConsolidated` data."""

    ano = serializers.IntegerField()

    cr_nu_area_ha = serializers.SerializerMethodField()
    dg_nu_area_ha = serializers.SerializerMethodField()
    dr_nu_area_ha = serializers.SerializerMethodField()
    ff_nu_area_ha = serializers.SerializerMethodField()
    total_nu_area_ha = serializers.SerializerMethodField()

    class Meta:
        """Meta class for `MonitoringConsolidatedByYearSerializer`
        serializer."""
        model = models.MonitoringConsolidated
        fields = [
            'ano',
            'cr_nu_area_ha',
            'dg_nu_area_ha',
            'dr_nu_area_ha',
            'ff_nu_area_ha',
            'total_nu_area_ha'
        ]

    # Métodos para formatação de campos de área
    def format_area(self, value):
        return locale.format_string("%.3f", value, grouping=True)

    def get_cr_nu_area_ha(self, obj):
        return self.format_area(obj['cr_nu_area_ha'])

    def get_dg_nu_area_ha(self, obj):
        return self.format_area(obj['dg_nu_area_ha'])

    def get_dr_nu_area_ha(self, obj):
        return self.format_area(obj['dr_nu_area_ha'])

    def get_ff_nu_area_ha(self, obj):
        return self.format_area(obj['ff_nu_area_ha'])

    def get_total_nu_area_ha(self, obj):
        return self.format_area(obj['total_nu_area_ha'])


class MonitoringConsolidatedByDaySerializer(serializers.ModelSerializer):
    """Serializer for table `models.MonitoringConsolidated` data."""

    cr_nu_area_ha = serializers.SerializerMethodField()
    dg_nu_area_ha = serializers.SerializerMethodField()
    dr_nu_area_ha = serializers.SerializerMethodField()
    ff_nu_area_ha = serializers.SerializerMethodField()
    total_nu_area_ha = serializers.SerializerMethodField()

    class Meta:
        """Meta class for `MonitoringConsolidatedByDaySerializer`
        serializer."""
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

    # Métodos para formatação de campos de área
    def format_area(self, value):
        return locale.format_string("%.3f", value, grouping=True)

    def get_cr_nu_area_ha(self, obj):
        return self.format_area(obj['cr_nu_area_ha'])

    def get_dg_nu_area_ha(self, obj):
        return self.format_area(obj['dg_nu_area_ha'])

    def get_dr_nu_area_ha(self, obj):
        return self.format_area(obj['dr_nu_area_ha'])

    def get_ff_nu_area_ha(self, obj):
        return self.format_area(obj['ff_nu_area_ha'])

    def get_total_nu_area_ha(self, obj):
        return self.format_area(obj['total_nu_area_ha'])
