from model_mommy.recipe import Recipe

from support.models import (
    LayersGroup,
    Geoserver,
    Layer,
    WmsLayer,
    TmsLayer,
    HeatmapLayer
)

from monitoring.models import MonitoringType


class Recipes:

    def __init__(self):
        self.geoserver_data = Recipe(
            Geoserver,
            name='Geoserver',
            wms_url='xskylab.com:8080/geoserver/',
            preview_url='xskylab.com:8080/geoserver/',
        )

        self.layers_group_data_1 = Recipe(
            LayersGroup,
            name='Test Layers Group 1',
            icon='layers',
            order='1',
        )

        self.layers_group_data_2 = Recipe(
            LayersGroup,
            name='Test Layers Group 2',
            icon='layers',
            order='2',
        )

        self.layer_data_1 = Recipe(
            Layer,
            name='Layer 1',
            order='1',
            layer_type='wms',
        )

        self.layer_data_2 = Recipe(
            Layer,
            name='Layer 2',
            order='2',
            layer_type='wms',
        )

        self.layer_data_3 = Recipe(
            Layer,
            name='Layer 3',
            layer_type='tms',
        )

        self.wms_layer_data = Recipe(
            WmsLayer,
            has_preview=False,
            has_detail=False,
            has_opacity=False,
            queryable=False,
            default_opacity=0,
            geoserver_layer_name='table_name',
            geoserver_layer_namespace='test',
        )

        self.tms_layer_data = Recipe(
            TmsLayer,
            url_tms='xskylab.com:8080/geoserver/',
            max_native_zoom=15,
            date='2020-01-01',
        )

        self.monitoring_type_data = Recipe(
            MonitoringType,
            name='Prodes',
            identifier='Prodes',
        )

        self.heatmap_layer_data = Recipe(
            HeatmapLayer,
        )