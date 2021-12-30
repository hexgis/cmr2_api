from django.test import TestCase
from django.db import transaction

from support import (
    models,
    recipes
)

from monitoring.models import MonitoringType


class TestGeoserverModel(TestCase):
    """ Test case for geoserver model """

    def setUp(self):
        """ Set up data for tests, created geoserver """

        self.recipes = recipes.Recipes()
        self.recipes.geoserver_data.make()

    def test_geoserver_data_creation(self):
        """ Test correct creation of geoserver """

        self.assertTrue(models.Geoserver.objects.count())

    def test_geoserver_post_save(self):
        """ Test get and access fields of geoserver model"""

        data = models.Geoserver.objects.first()
        self.assertTrue(data.name)
        self.assertTrue(data.wms_url)
        self.assertTrue(data.preview_url)


class TestLayersGroupModel(TestCase):
    """ Test case for Layers Group model """

    def setUp(self):
        """ Set up data for tests, created Layers Group """

        self.recipes = recipes.Recipes()
        self.recipes.layers_group_data_1.make()

    def test_layers_group_data_creation(self):
        """ Test correct creation of layers groups with different orders """

        self.assertTrue(models.LayersGroup.objects.count())
        self.recipes.layers_group_data_2.make()

        self.assertTrue(models.LayersGroup.objects.count() == 2)

    def test_layers_group_post_save(self):
        """ Test get and access to field of Layers Group """

        data = models.LayersGroup.objects.first()
        self.assertTrue(data.name)
        self.assertTrue(data.icon)
        self.assertTrue(data.order)

    def test_layers_group_unique_fields(self):
        """
        Test constraint of unique fields on layers groups (order and name)
        """

        self.recipes.layers_group_data_2.make()

        with transaction.atomic():
            with self.assertRaises(Exception):
                self.recipes.layers_group_data_2.make(
                    order='3'
                )

            with self.assertRaises(Exception):
                self.recipes.layers_group_data_2.make(
                    name='Test LayersGroup 3'
                )

        self.assertTrue(models.LayersGroup.objects.count() == 2)

        self.recipes.layers_group_data_2.make(
            name='Test LayersGroup 3',
            order='3'
        )
        self.assertTrue(models.LayersGroup.objects.count() == 3)


class TestLayerModel(TestCase):
    """ Test case for layer model """

    def setUp(self):
        """ Set up data for tests, created layer and
        foreign keys models (layers_group) """

        self.recipes = recipes.Recipes()
        self.recipes.layers_group_data_1.make()
        self.layers_group = models.LayersGroup.objects.first()

        self.recipes.layer_data_1.make(
            layers_group_id=self.layers_group.id
        )

    def test_layer_data_creation(self):
        """ Test layer creation """

        self.assertTrue(models.Layer.objects.count())

        self.recipes.layer_data_2.make(
            layers_group_id=self.layers_group.id
        )
        self.recipes.layer_data_3.make(
            layers_group_id=self.layers_group.id
        )

        self.assertTrue(models.Layer.objects.count() == 3)

    def test_layer_layers_group_relation(self):
        """ Test layer relation with layers_group and reverse access """

        self.layer = models.Layer.objects.first()

        self.assertTrue(self.layer.layers_group)
        self.assertTrue(self.layer.layers_group.layers.count() == 1)


class TestWmsLayerModel(TestCase):
    """ Test case for wmslayer model """

    def setUp(self):
        """ Set up data for tests, created wms layer and
        foreign keys models (layers_group, geoserver, layer) """

        self.recipes = recipes.Recipes()

        self.recipes.geoserver_data.make()
        self.geoserver = models.Geoserver.objects.first()

        self.recipes.layers_group_data_1.make()
        self.layers_group = models.LayersGroup.objects.first()

        self.recipes.layer_data_1.make(
            layers_group_id=self.layers_group.id
        )
        self.layer = models.Layer.objects.first()

    def test_wms_layer_data_creation(self):
        """ Test wms layer creation """

        self.assertEqual(models.WmsLayer.objects.count(), 0)

        self.recipes.wms_layer_data.make(
            layer_id=self.layer.id,
            geoserver_id=self.geoserver.id
        )

        self.assertTrue(models.WmsLayer.objects.count() == 1)

    def test_wms_layer_relation(self):
        """ Test wmslayer relation with layer and geoserver """

        self.recipes.wms_layer_data.make(
            layer_id=self.layer.id,
            geoserver_id=self.geoserver.id
        )

        self.wms_layer = models.WmsLayer.objects.first()

        self.assertTrue(self.wms_layer.layer)
        self.assertTrue(self.wms_layer.geoserver)


class TestTmsLayerModel(TestCase):
    """ Test case for tmslayer model """

    def setUp(self):
        """ Set up data for tests, created tmslayer and
        foreign keys models (layers_group, layer) """

        self.recipes = recipes.Recipes()

        self.recipes.layers_group_data_1.make()
        self.layers_group = models.LayersGroup.objects.first()

        self.recipes.layer_data_1.make(
            layers_group_id=self.layers_group.id
        )
        self.layer = models.Layer.objects.first()

    def test_tms_layer_data_creation(self):
        """ Test tmslayer creation """

        self.assertEqual(models.TmsLayer.objects.count(), 0)

        self.recipes.tms_layer_data.make(
            layer_id=self.layer.id,
        )

        self.assertTrue(models.TmsLayer.objects.count() == 1)

    def test_tms_layer_relation(self):
        """ Test tmslayer relation with layer """

        self.recipes.tms_layer_data.make(
            layer_id=self.layer.id,
        )

        self.tms_layer = models.TmsLayer.objects.first()
        self.assertTrue(self.tms_layer.layer)


class TestHeatmapLayerModel(TestCase):
    """ Test case for heatmap layer model """

    def setUp(self):
        """ Set up data for tests, created heatmap layer and
        foreign keys models (monitoring types, layer) """

        self.recipes = recipes.Recipes()

        self.recipes.layers_group_data_1.make()
        self.layers_group = models.LayersGroup.objects.first()

        self.recipes.layer_data_1.make(
            layers_group_id=self.layers_group.id
        )
        self.layer = models.Layer.objects.first()

        self.recipes.monitoring_type_data.make()
        self.monitoring_type = MonitoringType.objects.first()

    def test_heatmap_layer_data_creation(self):
        """ Test heatmap layer creation """

        self.assertEqual(HeatmapLayer.objects.count(), 0)

        self.recipes.heatmap_layer_data.make(
            layer_id=self.layer.id,
            heatmap_type_id=self.monitoring_type.id
        )

        self.assertTrue(HeatmapLayer.objects.count() == 1)

    def test_heatmap_layer_relation(self):
        """ Test heatmap layer relation with heatmap type """

        self.recipes.heatmap_layer_data.make(
            layer_id=self.layer.id,
            heatmap_type_id=self.monitoring_type.id
        )

        self.heatmap_layer = HeatmapLayer.objects.first()
        self.assertTrue(self.heatmap_layer.layer)
        self.assertTrue(self.heatmap_layer.heatmap_type)
