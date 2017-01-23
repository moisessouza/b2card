"use strict";

var inicialservices = angular.module('inicial-services', ['ngResource']);

inicialservices.config(['$resourceProvider', function($resourceProvider) {
	  // Don't strip trailing slashes from calculated URLs
	  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

inicialservices.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

inicialservices.service('InicialService', function($resource){
	return {
		buscaratividadesprofissional: function (callback){
			var Clientes = $resource(BASE_URL + 'inicial/api/atividadesprofissional/');
			return Clientes.query(callback);
		}
	}
});
