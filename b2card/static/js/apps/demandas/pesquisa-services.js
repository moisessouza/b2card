"use strict";

var pesquisademandaservices = angular.module('pesquisademanda-services', ['ui.bootstrap', 'commons', 'ui.mask',  'ngMaterial']);

pesquisademandaservices.config(['$resourceProvider', function($resourceProvider) {
	  // Don't strip trailing slashes from calculated URLs
	  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

pesquisademandaservices.config(['$httpProvider', function($httpProvider) {
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
	$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

pesquisademandaservices.service('PesquisaDemandaService', function($resource){
	return {
		buscardemandas: function(argumentos, callback){
			var Demandas = $resource(BASE_URL + 'demandas/api/query/', {}, {
				'set': {method:'POST'}
			});
			return Demandas.set({}, argumentos, callback);
		}
	}
});