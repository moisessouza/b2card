"use strict";

var orcamentosservices = angular.module('orcamentos-services', ['ngResource']);

orcamentosservices.config(['$resourceProvider', function($resourceProvider) {
	  // Don't strip trailing slashes from calculated URLs
	  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

orcamentosservices.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

orcamentosservices.service('OrcamentosService', function($resource){
	return {
		buscarorcamento: function(orcamento_id, callback){
			Orcamento = $resource('/orcamentos/api/:id')
			var result = Orcamento.get({id:orcamento_id}, callback);
			return result;
		},
		salvar: function(data, callback) {
			Orcamento = $resource('/orcamentos/api/save/');
			var result = Orcamento.save(data, function (data) {
				if (callback){
					callback(data);
				}
			});
			return result;
		}
	}
});
