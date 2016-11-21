"use strict";

var contagerencialservices = angular.module('contagerencial-services', ['ngResource']);

contagerencialservices.config(['$resourceProvider', function($resourceProvider) {
	  // Don't strip trailing slashes from calculated URLs
	  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

contagerencialservices.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

contagerencialservices.service('ContaGerencialService', function($resource){
	return {
		buscarcontagerenciais: function (callback) {
			var ContaGerencial = $resource('/cadastros/contagerencial/api/list/');
			return ContaGerencial.query(callback);
		},
		salvar: function(data, callback) {
			var ContaGerencial = $resource('/cadastros/contagerencial/api/detail/');
			return ContaGerencial.save(data, callback);
		},
		deletar: function(data, callback){
			var ContaGerencial = $resource('/cadastros/contagerencial/api/:id/');
			return ContaGerencial.remove({id: data.id}, data, callback);
		}
	}
});
