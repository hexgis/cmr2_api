MODULOS_CMR = {
    "catalog-tab": {
    	"access":{"catalog.access_satellite","catalog.access_scene"},
    	"description":"Meu acervo de imagens",
        "alias": "Catalogo"},
    "search-tab": {
    	"access":{"monitoring.access_monitoringconsolidated",},
    	"description":"Monitoramento Diário",
        "alias": "Monitoramento"},
    "layers-tab": {
    	"access":{"support.access_geoserver","support.access_categorylayersgroup","support.access_layersgroup","support.access_layer","support.access_wmslayer","support.access_tmslayer","support.access_layerfilter",},
    	"description":"Camadas de Sobreposição",
        "alias": "Apoio"},
    "high-resolution-mosaics-tab": {
    	"access":{"support.access_geoserver","support.access_categorylayersgroup","support.access_layersgroup","support.access_layer","support.access_wmslayer","support.access_tmslayer","support.access_layerfilter",},
    	"description":"Alta Resolução e Mosaicos",
        "alias": "Imagens"},
    "support-fire-tab": {
    	"access":{"support.access_geoserver","support.access_categorylayersgroup","support.access_layersgroup","support.access_layer","support.access_wmslayer","support.access_tmslayer","support.access_layerfilter",},
    	"description":"Risco de Fogo e Focos de Calor",
        "alias": "Fogo"},
    "landuse-tab": {
    	"access":{"land_use.access_landuseti","land_use.access_landuseclasses",},
    	"description":"Uso e Ocupação do Solo",
        "alias": "UOS"},
    "prodes-tab": {
    	"access":{"support.access_geoserver","support.access_categorylayersgroup","support.access_layersgroup","support.access_layer","support.access_wmslayer","support.access_tmslayer","support.access_layerfilter",},
    	"description":"PRODES (INPE)",
        "alias": "Prodes"},
    "urgent-alerts-tab": {
    	"access":{"priority_alerts.view_urgentalerts",},
    	"description":"Alerta Urgente",
        "alias": "Alertas"},
    "priority-tab": {
    	"access":{"priority_monitoring.access_priorityconsolidated",},
    	"description":"Polígonos Prioritários",
        "alias": "Prioritários"},
    "document-tab": {
    	"access":{"support.access_geoserver","support.access_categorylayersgroup","support.access_layersgroup","support.access_layer","support.access_wmslayer","support.access_tmslayer","support.access_layerfilter",},
    	"description":"Documental",
        "alias": "Documental"},
    "mapoteca-tab": {
    	"access":{"deter_monitoring.access_deterti",},
    	"description":"Deter",
        "alias": "Deter"}
}


GROUPS_CMR = [
	'FUNAI_SEDE',
	'FUANI_COORDENACAO_REGIONAL',
	'FUNAI_TERRA_INDIGENA',
	'FPE',
	'OUTRAS_INSTITUICOES',
	'ACADEMICO',
	'CULTURAL',
	'AUTENTICADO',
	'NAO_AUTENTICADO'
]


PROFILE_CMR = {
	"Catalogo (Visualizar)": {
		"access_catalogs","access_satellite","view_satellite","view_catalogs",},
	"Catalogo (Total)": {
		"access_satellite","view_satellite","add_satellite","change_satellite","delete_satellite","access_scene","view_scene","add_scene","change_scene","delete_scene",},
	"Funai_CGMT": {
		"PROFILE_CMR['Catalogo (Visualizar)']","PROFILE_CMR['Catalogo (Total)']",}
}
