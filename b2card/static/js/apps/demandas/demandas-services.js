var demandasservices = angular.module('demandas-services', ['ngResource']);

demandasservices.config(['$resourceProvider', function($resourceProvider) {
	  // Don't strip trailing slashes from calculated URLs
	  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

demandasservices.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

demandasservices.service('DemandaService', function($resource){
	return {
		buscarclientes: function(callback){
			var Clientes = $resource('/clientes/api/list')
			var result = Clientes.query(callback);
			return result;
		},
		buscarfuncionarios: function(callback){
			var Recursos = $resource('/recursos/api/list')
			var result = Recursos.query(callback);
			return result;
		},
		buscartipohoracliente: function(idcliente, callback){
			var Clientes = $resource('/clientes/api/cliente/:id/valorhora/')
			return Clientes.query({id:idcliente}, callback);
		},
		buscarcentroresultados: function(idcliente, callback){
			var Clientes = $resource('/clientes/api/cliente/:id/centroresultado/')
			return Clientes.query({id:idcliente}, callback);
		},
		salvardemanda: function(data, callback){
			var Demandas = $resource('/demandas/api/new/');
			return Demandas.save(data, callback);
		},
		buscardemanda: function(id, callback){
			var Demandas = $resource('/demandas/api/:id');
			return Demandas.get({id:id}, callback);
		},
		deletardemanda: function(id, callback){
			var Demandas = $resource('/demandas/api/:id');
			return Demandas.remove({id:id}, callback);
		}
	}
});
