"""Validar implementação de utils.py no APP DOCUMENTARY"""

# Funcao que retorna pasta para documentos de TI
def diretorio_ti(instance, filename):
    return "documentos_terra_indigena/{0}/{1}".format(instance.no_ti, filename)

# Funcao que retorna pasta para mapas de uso e ocupação do solo
def diretorio_mapas_uso_solo(instance, filename):
    return "mapas_uso_ocupacao_solo/{0}/{1}".format(instance.co_funai, filename)
