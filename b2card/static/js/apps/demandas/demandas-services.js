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
		buscarclientes: function(orcamento_id, callback){
			Clientes = $resource('/clientes/api/list')
			var result = Clientes.query({id:orcamento_id}, callback);
			return result;
		}
	}
});
