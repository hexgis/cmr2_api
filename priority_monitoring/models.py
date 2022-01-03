from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields import BooleanField


class PriorityConsolidatedTemp(models.Model):
    PRIORIDADE = (
        ('A', 'Alta'),
        ('M', 'Média'),
        ('B', 'Baixa')
    )

    no_estagio = models.CharField(
        #_("Estágio de Degradação"),
        max_length=255,
        blank=True,
        null=True,
    )
    no_cr = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    no_ti = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    ranking = models.IntegerField(
        null=True,
        blank=True,
    )
    prioridade = models.CharField(
        max_length=1,
        choices=PRIORIDADE,
        blank=True,
        null=True,
        default='B',
    )
    flag = BooleanField(
        default= False,
    )
    dt_t_um = models.DateField(
        null=True,
        blank=True,
    )
    geom = models.CharField(
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
        null=True,
        blank=True,
    )
    tb_ciclo_monitoramento_id = models.IntegerField(
        null=True,
        blank=True,
    )
    no_estagio = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    no_image = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    dt_image = models.DateField(
        null=True,
        blank=True,
    )
    nu_orbita = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    nu_ponto = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    dt_t0 = models.DateField(
        null=True,
        blank=True,
    )
    dt_t1 = models.DateField(
        null=True,
        blank=True,
    )
    nu_area_km2 = models.DecimalField(
        max_digits=20,
        decimal_places=15,
        null=True,
        blank=True,
    )
    nu_area_ha = models.DecimalField(
        max_digits=20,
        decimal_places=15,
        null=True,
        blank=True,
    )
    nu_latitude = models.DecimalField(
        max_digits=20,
        decimal_places=15,
        null=True,
        blank=True,
    )
    nu_longitude = models.DecimalField(
        max_digits=20,
        decimal_places=15,
        null=True,
        blank=True,
    )
    tempo = models.IntegerField(
        null=True,
        blank=True,
    )
    contribuicao = models.IntegerField(
        null=True,
        blank=True,
    )
    velocidade = models.DecimalField(
        max_digits=20,
        decimal_places=15,
        null=True,
        blank=True,
    )
    contiguidade = models.IntegerField(
        null=True,
        blank=True,
    )
    ranking = models.DecimalField(
        max_digits=20,
        decimal_places=15,
        null=True,
        blank=True,
    )
    prioridade = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    dt_cadastro = models.DateTimeField(
        null=True,
        blank=True,
    )
    geom = models.JSONField(
        _("Priority Consolidated Geometry"),
        null=True,
        blank=True,
    )





# class PriorityConsolidatedTb(models.Model):

#     tb_ciclo_monitoramento_id = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True,
#     )
#     no_estagio = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True,
# 	)
#     no_imagem = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True,
#     )
#     dt_imagem = models.DateField(
#         null=True,
#         blank=True,
# 	)
#     nu_orbita = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True,
# 	)
#     nu_ponto = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True,
# 	)
#     dt_t_zero = models.DateField(
#         null=True,
#         blank=True,
#     )
#     dt_t_um = models.DateField(
#         null=True,
#         blank=True,
# 	)
#     nu_area_km2 = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True,
# 	)
#     nu_area_ha = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True,
# 	)
#     nu_latitude = models.CharField(
#         max_length=512,
#         null=True,
#         blank=True,
# 	)
#     nu_longitude = models.CharField(
#         max_length=512,
#         null=True,
#         blank=True,
# 	)
#     tempo = models.IntegerField(
#         null=True,
#         blank=True,
# 	)
#     contribuicao = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True,
# 	)
#     velocidade = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True,
# 	)
#     contiguidade = models.IntegerField(
#         null=True,
#         blank=True,
# 	)
#     ranking = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True,
# 	)
#     prioridade = models.CharField(
#         max_length=255,
#         null=True,
#         blank=True,
# 	)
#     dt_cadastro = models.DateField(
#         null=True,
#         blank=True,
# 	)
#     co_uf = models.IntegerField(
#         null=True,
#         blank=True,
# 	)
#     co_municipio = models.IntegerField(
#         null=True,
#         blank=True,
# 	)
#     # geom = models.CharField(
#     #     max_length=255
# 	# )