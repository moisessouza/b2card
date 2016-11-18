var clientesservices = angular.module('tipohora-services', ['ngResource']);

clientesservices.config(['$resourceProvider', function($resourceProvider) {
	  // Don't strip trailing slashes from calculated URLs
	  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

clientesservices.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

clientesservices.service('TipoHoraService', function($resource){
	return {
		buscartipohoras: function (callback) {
			var TipoHora = $resource('/cadastros/tipohora/api/list/');
			return TipoHora.query(callback);
		},
		salvar: function(data, callback) {
			var TipoHora = $resource('/cadastros/tipohora/api/detail/');
			return TipoHora.save(data, callback);
		},
		deletar: function(data, callback){
			var TipoHora = $resource('/cadastros/tipohora/api/:id/');
			return TipoHora.remove({id: data.id}, data, callback);
		}
	}
});
