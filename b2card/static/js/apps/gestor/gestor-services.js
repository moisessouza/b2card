"use strict";

var gestorservices = angular.module('gestor-services', ['ngResource']);

gestorservices.config(['$resourceProvider', function($resourceProvider) {
	  // Don't strip trailing slashes from calculated URLs
	  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

gestorservices.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

gestorservices.service('GestorService', function($resource){
	return {
		buscarclientesdemandas: function (argumento, callback){
			var Clientes = $resource(BASE_URL + 'gestor/api/clientesdemandas/', {},{
				'set': {method:'POST', isArray: true}
			});
			return Clientes.set({}, argumento, callback);
		}
	}
});
