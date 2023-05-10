CMR_MODULES = {
    "catalog-tab": {
    	"access":{"catalog.access_satellite","catalog.access_scene",},
    	"description":"Meu acervo de imagens",
        "alias": "Catalogo"},
    "search-tab": {
    	"access":{"monitoring.access_monitoringconsolidated","funai.access_coordenacaoregional","funai.access_limiteterraindigena"},
    	"description":"Monitoramento Diário",
        "alias": "Monitoramento"},
    "layers-tab": {
    	"access":{"support.access_geoserver","support.access_categorylayersgroup","support.access_layersgroup","support.access_layer","support.access_wmslayer","support.access_tmslayer","support.access_layerfilter","funai.access_coordenacaoregional","funai.access_limiteterraindigena"},
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
    	"access":{"land_use.access_landuseti","land_use.access_landuseclasses","funai.access_coordenacaoregional","funai.access_limiteterraindigena"},
    	"description":"Uso e Ocupação do Solo",
        "alias": "UOS"},
    "prodes-tab": {
    	"access":{"support.access_geoserver","support.access_categorylayersgroup","support.access_layersgroup","support.access_layer","support.access_wmslayer","support.access_tmslayer","support.access_layerfilter","funai.access_coordenacaoregional","funai.access_limiteterraindigena"},
    	"description":"PRODES (INPE)",
        "alias": "Prodes"},
    "urgent-alerts-tab": {
    	"access":{"priority_alerts.access_urgentalerts","funai.access_coordenacaoregional","funai.access_limiteterraindigena"},
    	"description":"Alerta Urgente",
        "alias": "Alertas"},
    "priority-tab": {
    	"access":{"priority_monitoring.access_priorityconsolidated","funai.access_coordenacaoregional","funai.access_limiteterraindigena"},
    	"description":"Polígonos Prioritários",
        "alias": "Prioritários"},
    "document-tab": {
    	"access":{"support.access_geoserver","support.access_categorylayersgroup","support.access_layersgroup","support.access_layer","support.access_wmslayer","support.access_tmslayer","support.access_layerfilter","funai.access_coordenacaoregional","funai.access_limiteterraindigena"},
    	"description":"Documental",
        "alias": "Documental"},
    "mapoteca-tab": {
    	"access":{"deter_monitoring.access_deterti","funai.access_coordenacaoregional","funai.access_limiteterraindigena"},
    	"description":"Deter",
        "alias": "Deter"}
}
"""
Lists all 'CMR2 Modules'.
Each 'CMR2 Module' key has in its value the information of:
	* access (set): Access to 'CMR2 Module'. List of all models used and
	necessary for the operation of this 'CMR2 Module'.
	* description (str): Description of 'CMR2 Module'.
	* alias (str): Usual name of 'CMR2 Module'.
"""


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
	"TI CR (Visualizar)": {
		"funai.access_coordenacaoregional","funai.access_limiteterraindigena","funai.view_coordenacaoregional","funai.view_limiteterraindigena",},
	"Catalogo (Visualizar)": {
		"access_catalogs","access_satellite","view_satellite","view_catalogs",},
	"Catalogo (Total)": {
		"access_satellite","view_satellite","add_satellite","change_satellite","delete_satellite","access_scene","view_scene","add_scene","change_scene","delete_scene",},
	"Funai_CGMT": {
		"PROFILE_CMR['Catalogo (Visualizar)']","PROFILE_CMR['Catalogo (Total)']",}
}
