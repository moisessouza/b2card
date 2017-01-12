"use strict";

var clientesservices = angular.module('fase-services', ['ngResource']);

clientesservices.config(['$resourceProvider', function($resourceProvider) {
	  // Don't strip trailing slashes from calculated URLs
	  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

clientesservices.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

clientesservices.service('FaseService', function($resource){
	return {
		buscarfases: function (callback) {
			var Fase = $resource(BASE_URL + 'cadastros/fase/api/list/');
			return Fase.query(callback);
		},
		salvar: function(data, callback) {
			var Fase = $resource(BASE_URL + 'cadastros/fase/api/detail/');
			return Fase.save(data, callback);
		},
		deletar: function(data, callback){
			var Fase = $resource(BASE_URL + 'cadastros/fase/api/:id/');
			return Fase.remove({id: data.id}, data, callback);
		}
	}
});
