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
			Clientes = $resource('/clientes/api/list')
			var result = Clientes.query(callback);
			return result;
		},
		buscarfuncionarios: function(callback){
			Recursos = $resource('/recursos/api/list')
			var result = Recursos.query(callback);
			return result;
		},
		buscartipohoracliente: function(idcliente, callback){
			Clientes = $resource('/clientes/api/cliente/:id/valorhora/')
			return Clientes.query({id:idcliente}, callback);
		},
		salvardemanda: function(data, callback){
			Demandas = $resource('/demandas/api/new/');
			return Demandas.save(data, callback);
		},
		buscardemanda: function(id, callback){
			Demandas = $resource('/demandas/api/:id');
			return Demandas.get({id:id}, callback);
		},
		deletardemanda: function(id, callback){
			Demandas = $resource('/demandas/api/:id');
			return Demandas.remove({id:id}, callback);
		}
	}
});
