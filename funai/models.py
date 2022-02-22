from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class CoordenacaoRegional(models.Model):
    """Models for Regional Coordenation."""

    co_cr = models.BigIntegerField(
        _('Regional Coordenation code'),
        unique=True,
        primary_key=True,
        default=1
    )

    no_cr = models.CharField(
        _('Regional Coordenation name'),
        max_length=255,
        blank=True,
        null=True
    )

    no_abreviado = models.CharField(
        _('Regional Coordenation acronym'),
        max_length=255,
        blank=True,
        null=True
    )

    sg_cr = models.CharField(
        _('Regional Coordenation flag'),
        max_length=255,
        blank=True,
        null=True
    )

    st_situacao = models.CharField(
        _('Situation'),
        max_length=255,
        blank=True,
        null=True
    )

    ds_email = models.CharField(
        _('Email'),
        max_length=255,
        blank=True,
        null=True
    )

    no_regiao = models.CharField(
        _('Region name'),
        max_length=255,
        blank=True,
        null=True
    )

    no_municipio = models.CharField(
        _('City name'),
        max_length=255,
        blank=True,
        null=True
    )

    no_uf = models.CharField(
        _('State'),
        max_length=255,
        blank=True,
        null=True
    )

    sg_uf = models.CharField(
        _('State acronym'),
        max_length=255,
        blank=True,
        null=True
    )

    ds_telefone = models.CharField(
        _('Contact number'),
        max_length=512,
        blank=True,
        null=True
    )

    dt_cadastro = models.DateTimeField(
        _('Register date'),
        blank=True,
        null=True
    )

    class Meta:
        """Metaclass to `funai.CoordenacaoRegional`."""
        app_label = 'funai'
        verbose_name = 'CoordenacaoRegional'
        verbose_name_plural = 'CoordenacoesRegionais'
        ordering = ('no_cr', )

    def __str__(self) -> str:
        """Returns string for class based name.

        Returns:
            str: string for model data
        """
        return f'{self.co_cr} - {self.no_cr}'


class LimiteTerraIndigena(models.Model):
    """Indigenous Lands model data.

    * Association:
        * Has one: `funai.CoordenacaoRegional`
    """

    co_funai = models.IntegerField(
        _('Funai code'),
        unique=True,
        blank=True,
        null=True
    )

    no_ti = models.CharField(
        _('Name of Indigenous Lands'),
        max_length=255,
        blank=True,
        null=True
    )

    ds_fase_ti = models.CharField(
        _('Description for TI stage'),
        max_length=255,
        blank=True,
        null=True
    )

    ds_modalidade = models.CharField(
        _('Modality'),
        max_length=255,
        blank=True,
        null=True
    )

    co_cr = models.ForeignKey(
        'funai.CoordenacaoRegional',
        on_delete=models.DO_NOTHING,
        related_name='cr',
        null=True
    )

    ds_cr = models.CharField(
        _('Description for Regional Coordination'),
        max_length=255,
        blank=True,
        null=True
    )

    sg_uf = models.CharField(
        _('State aconymn'),
        max_length=255,
        blank=True,
        null=True
    )

    nu_area_ha = models.DecimalField(
        _('Area ha'),
        max_digits=19,
        decimal_places=10,
        blank=True,
        null=True
    )

    nu_area_km = models.DecimalField(
        _('Area km'),
        max_digits=19,
        decimal_places=10,
        blank=True,
        null=True
    )

    st_faixa_fronteira = models.CharField(
        _('Border strip'),
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        """Metaclass to `funai.LimiteTerraIndigena`."""
        app_label = 'funai'
        verbose_name = _('Indigenous Lands')
        verbose_name_plural = _('Indigenous Lands')
        ordering = ('-no_ti', )
