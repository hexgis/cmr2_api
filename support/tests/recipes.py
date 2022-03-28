from model_mommy.recipe import Recipe

from support import models


class Recipes:

    def __init__(self):
        self.geoserver_data = Recipe(
            models.Geoserver,
            name='Geoserver',
            wms_url='xskylab.com:8080/geoserver/',
            preview_url='xskylab.com:8080/geoserver/',
        )

        self.layers_group_data_1 = Recipe(
            models.LayersGroup,
            name='Test Layers Group 1',
            icon='layers',
            order='1',
        )

        self.layers_group_data_2 = Recipe(
            models.LayersGroup,
            name='Test Layers Group 2',
            icon='layers',
            order='2',
        )

        self.layer_data_1 = Recipe(
            models.Layer,
            name='Layer 1',
            order='1',
            layer_type='wms',
        )

        self.layer_data_2 = Recipe(
            models.Layer,
            name='Layer 2',
            order='2',
            layer_type='wms',
        )

        self.layer_data_3 = Recipe(
            models.Layer,
            name='Layer 3',
            layer_type='tms',
        )

        self.wms_layer_data = Recipe(
            models.WmsLayer,
            has_preview=False,
            has_detail=False,
            has_opacity=False,
            queryable=False,
            default_opacity=0,
            geoserver_layer_name='table_name',
            geoserver_layer_namespace='test',
        )

        self.tms_layer_data = Recipe(
            models.TmsLayer,
            url_tms='xskylab.com:8080/geoserver/',
            max_native_zoom=15,
            date='2020-01-01',
        )
