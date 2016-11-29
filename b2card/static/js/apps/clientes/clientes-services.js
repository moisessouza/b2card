"use strict";

var clientesservices = angular.module('clientes-services', ['ngResource']);

clientesservices.config(['$resourceProvider', function($resourceProvider) {
	  // Don't strip trailing slashes from calculated URLs
	  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

clientesservices.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

clientesservices.service('ClientesService', function($resource){
	return {
		buscarcliente: function(id, callback){
			var Cliente = $resource('/clientes/api/:id/');
			return Cliente.get({id:id}, callback);
		},
		salvarcliente: function(cliente, callback){
			var Cliente = $resource('/clientes/api/new/');
			return Cliente.save(cliente, callback);
		},
		deletarcliente: function(cliente, callback){
			var Cliente = $resource('/clientes/api/:id/');
			return Cliente.remove({id: cliente.id}, callback);
		}
	}
});
