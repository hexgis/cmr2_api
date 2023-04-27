MODULOS_CMR = {
    "catalog-tab": {
    	"access":{"access_satellite","access_scene"},
    	"description":"Meu acervo de imagens",
        "alias": "Catalogo"},
    "search-tab": {
    	"access":{"access_monitoringconsolidated",},
    	"description":"Monitoramento Diário",
        "alias": "Monitoramento"},
    "layers-tab": {
    	"access":{"access_geoserver","access_categorylayersgroup","access_layersgroup","access_layer","access_wmslayer","access_tmslayer","access_layerfilter",},
    	"description":"Camadas de Sobreposição",
        "alias": "Apoio"},
    "high-resolution-mosaics-tab": {
    	"access":{"access_geoserver","access_categorylayersgroup","access_layersgroup","access_layer","access_wmslayer","access_tmslayer","access_layerfilter",},
    	"description":"Alta Resolução e Mosaicos",
        "alias": "Imagens"},
    "support-fire-tab": {
    	"access":{"access_geoserver","access_categorylayersgroup","access_layersgroup","access_layer","access_wmslayer","access_tmslayer","access_layerfilter",},
    	"description":"Risco de Fogo e Focos de Calor",
        "alias": "Fogo"},
    "landuse-tab": {
    	"access":{"access_landuseti","access_landuseclasses",},
    	"description":"Uso e Ocupação do Solo",
        "alias": "UOS"},
    "prodes-tab": {
    	"access":{"access_geoserver","access_categorylayersgroup","access_layersgroup","access_layer","access_wmslayer","access_tmslayer","access_layerfilter",},
    	"description":"PRODES (INPE)",
        "alias": "Prodes"},
    "urgent-alerts-tab": {
    	"access":{"access_urgentalerts",},
    	"description":"Alerta Urgente",
        "alias": "Alertas"},
    "priority-tab": {
    	"access":{"access_priorityconsolidated",},
    	"description":"Polígonos Prioritários",
        "alias": "Prioritários"},
    "document-tab": {
    	"access":{"access_docsaction","access_userscmr","access_docslanduser","access_docsdocumentti","access_docsmapoteca","access_userscmr",},
    	"description":"Documental",
        "alias": "Documental"},
    "mapoteca-tab": {
    	"access":{"access_deterti",},
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
