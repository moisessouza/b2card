"use strict";

var inicialservices = angular.module('inicial-services', ['ngResource']);

inicialservices.config(['$resourceProvider', function($resourceProvider) {
	  // Don't strip trailing slashes from calculated URLs
	  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

inicialservices.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

inicialservices.service('InicialService', function($resource){
	return {
		buscaratividadesprofissional: function (argumento, callback){
			var Clientes = $resource(BASE_URL + 'inicial/api/atividadesprofissional/', {}, {
				'set':{method:'POST', isArray: true}
			});
			return Clientes.set({}, argumento, callback);
		},
		salvaralocacao: function (data, callback) {
			var AlocacaoHoras = $resource(BASE_URL + 'inicial/api/alocacao/');
			return AlocacaoHoras.save({}, data, callback);
		},
		buscarultimaalocacao: function (alocacao_id, callback){
			var AlocacaoHoras = $resource(BASE_URL + 'inicial/api/ultimaalocacao/:id/');
			return AlocacaoHoras.get({id:alocacao_id}, callback);
		},
		buscaratividadesprofissionalporatividade: function (atividade_id, callback){
			var AtividadeProfissional = $resource(BASE_URL + 'inicial/api/atividadesprofissional/:id/');
			return AtividadeProfissional.get({id:atividade_id}, callback);
		},
		buscaratividadesprofissionalpordemandaid: function (demanda_id, callback) {
			var AtividadeProfissional = $resource(BASE_URL + 'inicial/api/atividadesprofissional/demanda/:id/');
			return AtividadeProfissional.query({id:demanda_id}, callback);
		},
		buscaratividadesinternas: function (argumento, callback){
			var Clientes = $resource(BASE_URL + 'inicial/api/atividadesinternas/', {}, {
				'set':{method:'POST', isArray: true}
			});
			return Clientes.set({}, argumento, callback);
		},
		buscaratividadesdemandainterna: function(demanda_id, callback) {
			var AtividadeProfissional = $resource(BASE_URL + 'inicial/api/atividadesinternas/demanda/:id/');
			return AtividadeProfissional.query({id:demanda_id}, callback);
		},
		salvaralocacaointerna: function(data, callback){
			var AlocacaoHoras = $resource(BASE_URL + 'inicial/api/alocacaointerna/');
			return AlocacaoHoras.save({}, data, callback);
		},
		verificarsepossuivigencia: function(date, callback) {
			var CustoPrestador = $resource(BASE_URL + 'inicial/api/verificar_se_possui_vigencia/:data_informada/');
			return CustoPrestador.get({data_informada: date}, callback);
		}
	}
});
