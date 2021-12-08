from django.db import transaction
import json

from .models import (
    LayersGroup,
    Layer
)


@transaction.atomic
def createLayersData(
    jsonPath=None,
    layers_group=None,
    quiet=False
):
    """
    *Create Monitoring Data using ReadGeojson class*

    Creates models data from ReadGeojson.getData() generator

    Arguments:
        * jsonPath (str): Path to json to create Data
        * driverName (str): Driver used to read datasource
        * fields (list): fields to parse
            a list of tuples with ModelAttribute and DataSource Attribute
            E.g.:[("class", "dn"), ("image","image_attr"))
        * dateFormat (str): date format to parse date from input data
            E.g.: "%d-%m-%y", "%d/%m/%y"
        * dateFormat (str): date format to parse date from input data
        * quiet (bool): used to verbose

     Returns:
        * created (int): created data length
    """

    if not jsonPath:
        raise ValueError("jsonPath is missing")

    data_created = []

    json_data = open('support/camadas_tms.json').read()
    data_json = json.loads(json_data)

    if layers_group:
        layers_group_object = LayersGroup.objects.get(id=layers_group)
        if not layers_group_object:
            raise ValueError("layers group not exists")
    else:
        last_order = LayersGroup.objects.order_by('-order').first().order
        last_order += 1
        layers_group_object = LayersGroup.objects.create(
            name="Nova Aba", order=last_order, icon="layers")

    for data in data_json:
        if not quiet:
            print(data)

        data['layers_group_id'] = layers_group_object.id
        created = Layer.objects.get_or_create(**data)
        if created:
            data_created.append(data)

    return len(data_created)
