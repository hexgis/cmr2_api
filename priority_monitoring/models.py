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




