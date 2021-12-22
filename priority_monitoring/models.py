from django.db import models
from django.db.models.fields import BooleanField




class PriorityConsolidated(models.Model):
    PRIORIDADE = (
        ('A', 'Alta'),
        ('M', 'Média'),
        ('B', 'Baixa')
    )

    no_estagio = models.CharField(
        #_("Estágio de Degradação"),
        max_length=255,
        blank=True,
        null=True
    )
    no_cr = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )
    no_ti = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )
    ranking = models.IntegerField(
        null=True
    )
    prioridade = models.CharField(
        max_length=1,
        choices=PRIORIDADE,
        blank=False,
        null=False,
        default='B'
    )
    flag = BooleanField(
    )
    dt_t_um = models.DateField(
    )
    geom = models.CharField(
        max_length=255,
        default='000'
    )

    def __str__(self):
        return  f'{self.no_estagio}:{self.ranking}'
        # return "{}:{}".format(
        #     self.id,
        #     self.prioridade
        # )



class PriorityConsolidatedTb(models.Model):

    tb_ciclo_monitoramento_id = models.CharField(
        max_length=255
    )
    no_estagio = models.CharField(
        max_length=255
	)
    no_imagem = models.CharField(
        max_length=255
    )
    dt_imagem = models.DateField(
	)
    nu_orbita = models.CharField(
        max_length=255
	)
    nu_ponto = models.CharField(
        max_length=255
	)
    dt_t_zero = models.DateField(
    )
    dt_t_um = models.DateField(
	)
    nu_area_km2 = models.CharField(
        max_length=255
	)
    nu_area_ha = models.CharField(
        max_length=255
	)
    nu_latitude = models.CharField(
        max_length=512
	)
    nu_longitude = models.CharField(
        max_length=512
	)
    tempo = models.IntegerField(
	)
    contribuicao = models.CharField(
        max_length=255
	)
    velocidade = models.CharField(
        max_length=255
	)
    contiguidade = models.IntegerField(
	)
    ranking = models.CharField(
        max_length=255
	)
    prioridade = models.CharField(
        max_length=255
	)
    dt_cadastro = models.DateField(
	)
    co_uf = models.IntegerField(
	)
    co_municipio = models.IntegerField(
	)
    # geom = models.CharField(
    #     max_length=255
	# )