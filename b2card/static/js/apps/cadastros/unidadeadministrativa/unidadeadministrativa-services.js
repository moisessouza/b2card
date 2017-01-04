"use strict";

var centrocustoservices = angular.module('unidadeadministrativa-services', ['ngResource']);

centrocustoservices.config(['$resourceProvider', function($resourceProvider) {
	  // Don't strip trailing slashes from calculated URLs
	  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

centrocustoservices.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

centrocustoservices.service('UnidadeAdministrativaService', function($resource){
	return {
		buscarunidadeadministrativas: function (callback) {
			var UnidadeAdministrativa = $resource(BASE_URL + 'cadastros/unidadeadministrativa/api/list/');
			return UnidadeAdministrativa.query(callback);
		},
		salvar: function(data, callback) {
			var UnidadeAdministrativa = $resource(BASE_URL + 'cadastros/unidadeadministrativa/api/detail/');
			return UnidadeAdministrativa.save(data, callback);
		},
		deletar: function(data, callback){
			var UnidadeAdministrativa = $resource(BASE_URL + 'cadastros/unidadeadministrativa/api/:id/');
			return UnidadeAdministrativa.remove({id: data.id}, data, callback);
		}
	}
});
