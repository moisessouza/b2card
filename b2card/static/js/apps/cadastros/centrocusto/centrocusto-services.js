"use strict";

var centrocustoservices = angular.module('centrocusto-services', ['ngResource']);

centrocustoservices.config(['$resourceProvider', function($resourceProvider) {
	  // Don't strip trailing slashes from calculated URLs
	  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

centrocustoservices.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

centrocustoservices.service('CentroCustoService', function($resource){
	return {
		buscarcentrocustos: function (callback) {
			var CentroCusto = $resource(BASE_URL + 'cadastros/centrocusto/api/list/');
			return CentroCusto.query(callback);
		},
		salvar: function(data, callback) {
			var CentroCusto = $resource(BASE_URL + 'cadastros/centrocusto/api/detail/');
			return CentroCusto.save(data, callback);
		},
		deletar: function(data, callback){
			var CentroCusto = $resource(BASE_URL + 'cadastros/centrocusto/api/:id/');
			return CentroCusto.remove({id: data.id}, data, callback);
		}
	}
});
