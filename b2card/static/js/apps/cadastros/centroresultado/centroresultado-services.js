"use strict";

var centroresultadoservices = angular.module('centroresultado-services', ['ngResource']);

centroresultadoservices.config(['$resourceProvider', function($resourceProvider) {
	  // Don't strip trailing slashes from calculated URLs
	  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

centroresultadoservices.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

centroresultadoservices.service('CentroResultadoService', function($resource){
	return {
		buscarcentroresultados: function (callback) {
			var CentroResultado = $resource('/cadastros/centroresultado/api/list/');
			return CentroResultado.query(callback);
		},
		salvar: function(data, callback) {
			var CentroResultado = $resource('/cadastros/centroresultado/api/detail/');
			return CentroResultado.save(data, callback);
		},
		deletar: function(data, callback){
			var CentroResultado = $resource('/cadastros/centroresultado/api/:id/');
			return CentroResultado.remove({id: data.id}, data, callback);
		}
	}
});
