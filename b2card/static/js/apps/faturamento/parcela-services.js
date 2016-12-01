"use strict";

var parcelaservices = angular.module('parcela-services', ['ngResource']);

parcelaservices.config(['$resourceProvider', function($resourceProvider) {
	  // Don't strip trailing slashes from calculated URLs
	  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

parcelaservices.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

parcelaservices.service('ParcelaService', function($resource){
	return {
		gravarparcelas: function (parcelas, callback){
			var Parcela = $resource('/faturamento/api/parcela/new/');
			return Parcela.save({}, parcelas, callback);
		},
		buscartotalhoras: function (demanda_id, callback){
			var Orcamento = $resource('/demandas/api/:id/orcamento/totalhoras/');
			return Orcamento.get({id:demanda_id}, callback);
		}
	}
});
