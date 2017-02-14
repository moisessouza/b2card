"use strict";

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
		buscarclientes: function(callback){
			var Clientes = $resource(BASE_URL + 'clientes/api/list')
			var result = Clientes.query(callback);
			return result;
		},
		buscarfuncionarios: function(callback){
			var Recursos = $resource(BASE_URL + 'recursos/api/list')
			var result = Recursos.query(callback);
			return result;
		},
		salvardemanda: function(data, callback){
			var Demandas = $resource(BASE_URL + 'demandas/api/new/');
			return Demandas.save(data, callback);
		},
		buscardemanda: function(id, callback){
			var Demandas = $resource(BASE_URL + 'demandas/api/:id');
			return Demandas.get({id:id}, callback);
		},
		deletardemanda: function(id, callback){
			var Demandas = $resource(BASE_URL + 'demandas/api/:id');
			return Demandas.remove({id:id}, callback);
		},
		buscarcentroresultadoshora: function(demanda_id, callback){
			var Demandas = $resource(BASE_URL + 'demandas/api/:id/centroresultadoshora/');
			return Demandas.query({id:demanda_id}, callback);
		},
		verificarseatividadeprofissionalpossuialocacao: function(atividade_profissional_id, callback) {
			var AlocacaoHoras = $resource(BASE_URL + 'demandas/api/profissionalatividade/:id/possuialocacao/');
			return AlocacaoHoras.get({id: atividade_profissional_id}, callback);
		},
		verificarseatividadepossuialocacao: function(atividade_id, callback) {
			var AlocacaoHoras = $resource(BASE_URL + 'demandas/api/atividade/:id/possuialocacao/');
			return AlocacaoHoras.get({id: atividade_id}, callback);
		},
		buscardemandaportexto: function(p, callback) {
			var Demandas = $resource(BASE_URL + 'demandas/api/texto/:texto/');
			return Demandas.query({texto:p}, callback);
		},
		buscaratividadesdemanda: function(demanda_id, callback){
			var Atividades = $resource(BASE_URL + 'demandas/api/:id/atividades/');
			return Atividades.query({id:demanda_id}, callback);
		}
	}
});
