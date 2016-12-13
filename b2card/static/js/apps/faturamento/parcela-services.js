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
		gravarparcelas: function (objeto, callback){
			var Parcela = $resource('/faturamento/api/parcela/new/', {}, {'save':  {
																						method:'POST', 
																						//isArray:true
																					}
																		 });
			return Parcela.save(objeto, callback);
		},
		buscartotalhoras: function (demanda_id, callback){
			var Orcamento = $resource('/demandas/api/:id/orcamento/totalhoras/');
			return Orcamento.get({id:demanda_id}, callback);
		},
		buscartotalhorasporvalorhora: function(demanda_id, callback){
			var Orcamento = $resource('/demandas/api/:id/orcamento/totalhoras/valorhora/');
			return Orcamento.query({id: demanda_id}, callback);
		},
		buscarparcelageradas: function(demanda_id, callback){
			var Parcela = $resource('/faturamento/api/parcela/demanda/:demanda_id/');
			return Parcela.query({demanda_id: demanda_id}, callback);
		}
	}
});
