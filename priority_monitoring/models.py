from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields import BooleanField


class PriorityConsolidatedTemp(models.Model):
    PRIORIDADE = (
        ('A', 'Alta'),
        ('M', 'Média'),
        ('B', 'Baixa')
    )

    no_estagio = models.CharField(
        # _('Estágio Classificação da Degradação'),
        max_length=255,
        blank=True,
        null=True,
    )

    no_cr = models.CharField(
        # _(''),
        max_length=255,
        blank=True,
        null=True,
    )

    no_ti = models.CharField(
        # _(''),
        max_length=255,
        blank=True,
        null=True,
    )

    ranking = models.IntegerField(
        # _(''),
        null=True,
        blank=True,
    )

    prioridade = models.CharField(
        # _(''),
        max_length=1,
        choices=PRIORIDADE,
        blank=True,
        null=True,
        default='B',
    )

    flag = BooleanField(
        # _(''),
        default= False,
    )

    dt_t_um = models.DateField(
        # _(''),
        null=True,
        blank=True,
    )

    geom = models.CharField(
        # _(''),
        max_length=255,
        null=True,
        blank=True,
        default='000',
    )

    def __str__(self):
        return  f'{self.no_estagio}:{self.ranking}'
        # return "{}:{}".format(
        #     self.id,
        #     self.prioridade
        # )


class PriorityConsolidated(models.Model):

    id_tb = models.IntegerField(
        # _(''),
        null=True,
        blank=True,
    )

    tb_ciclo_monitoramento_id = models.IntegerField(
        # _(''),
        null=True,
        blank=True,
    )

    no_estagio = models.CharField(
        # _(''),
        max_length=255,
        null=True,
        blank=True,
    )

    no_image = models.CharField(
        # _(''),
        max_length=255,
        null=True,
        blank=True,
    )

    dt_image = models.DateField(
        # _(''),
        null=True,
        blank=True,
    )

    nu_orbita = models.CharField(
        # _(''),
        max_length=255,
        null=True,
        blank=True,
    )

    nu_ponto = models.CharField(
        # _(''),
        max_length=255,
        null=True,
        blank=True,
    )

    dt_t0 = models.DateField(
        # _(''),
        null=True,
        blank=True,
    )

    dt_t1 = models.DateField(
        # _(''),
        null=True,
        blank=True,
    )

    nu_area_km2 = models.DecimalField(
        # _(''),
        max_digits=20,
        decimal_places=15,
        null=True,
        blank=True,
    )

    nu_area_ha = models.DecimalField(
        # _(''),
        max_digits=20,
        decimal_places=15,
        null=True,
        blank=True,
    )

    nu_latitude = models.DecimalField(
        # _(''),
        max_digits=20,
        decimal_places=15,
        null=True,
        blank=True,
    )

    nu_longitude = models.DecimalField(
        # _(''),
        max_digits=20,
        decimal_places=15,
        null=True,
        blank=True,
    )

    tempo = models.IntegerField(
        # _(''),
        null=True,
        blank=True,
    )

    contribuicao = models.IntegerField(
        # _(''),
        null=True,
        blank=True,
    )

    velocidade = models.DecimalField(
        # _(''),
        max_digits=20,
        decimal_places=15,
        null=True,
        blank=True,
    )

    contiguidade = models.IntegerField(
        # _(''),
        null=True,
        blank=True,
    )

    ranking = models.DecimalField(
        # _(''),
        max_digits=20,
        decimal_places=15,
        null=True,
        blank=True,
    )

    prioridade = models.CharField(
        # _(''),
        max_length=255,
        null=True,
        blank=True,
    )

    dt_cadastro = models.DateTimeField(
        # _(''),
        null=True,
        blank=True,
    )

    geom = models.GeometryField(
        _('Geometry Field'),
        srid=4326,
        blank=True,
        null=True,
    )

    class Meta:
        app_label = 'priority_monitoring'
        verbose_name = 'PriorityConsolidated'
        verbose_name_plural = 'PrioritysConsolidated'
        ordering = ["-dt_t0","ranking","no_estagio"]