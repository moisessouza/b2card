"use strict";

var relatorio_lancamentos = angular.module('relatorio_lancamentos-services', ['ngResource']);

relatorio_lancamentos.config(['$resourceProvider', function($resourceProvider) {
	  // Don't strip trailing slashes from calculated URLs
	  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

relatorio_lancamentos.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

relatorio_lancamentos.service('RelatorioLancamentosService', function($resource){
	return {
		pesquisar: function (argumentos, callback) {
			var AlocacaoHoras = $resource(BASE_URL + 'relatorio_lancamentos/api/search/', {}, {
				'set': {method:'POST', isArray: true}
			});
			return AlocacaoHoras.set({}, argumentos, callback);
		},
		salvaralocacao: function(data, callback) {
			var AlocacaoHoras =  $resource(BASE_URL + 'relatorio_lancamentos/api/alocarhoras/');
			return AlocacaoHoras.save({}, data, callback);
		},
		salvaralocacaointerna: function(data, callback) {
			var AlocacaoHoras =  $resource(BASE_URL + 'relatorio_lancamentos/api/alocarhorasinternas/');
			return AlocacaoHoras.save({}, data, callback);
		},
		ehgestor: function(callback) {
			var EhGestor =  $resource(BASE_URL + 'relatorio_lancamentos/api/eh_gestor/');
			return EhGestor.get(callback);
		},
		validardatahora: function(alocacao_id, data, hora_inicio, hora_fim, callback) {
			var CustoPrestador = $resource(BASE_URL + 'relatorio_lancamentos/api/validar_data_hora/:alocacao_id/:data_informada/:hora_inicio/:hora_fim/');
			return CustoPrestador.get({'alocacao_id': alocacao_id, 'data_informada': data, 'hora_inicio': hora_inicio, 'hora_fim': hora_fim}, callback);
		},
		verificartipodemanda: function(alocacao_id, callback) {
			var TipoDemanda = $resource(BASE_URL + 'relatorio_lancamentos/api/verificar_tipo_demanda/:alocacao_id/');
			return TipoDemanda.get({'alocacao_id': alocacao_id}, callback);
		},
		excluiralocacao: function (alocacao_id, callback) {
			var AlocacaoHoras =  $resource(BASE_URL + 'relatorio_lancamentos/api/:alocacao_id/excluir/');
			return AlocacaoHoras.remove({'alocacao_id': alocacao_id}, callback)
		},
		excluiralocacaointerna: function (alocacao_id, callback) {
			var AlocacaoHoras =  $resource(BASE_URL + 'relatorio_lancamentos/api/:alocacao_id/excluir_alocacao_interna/');
			return AlocacaoHoras.remove({'alocacao_id': alocacao_id}, callback)
		}
	}
});
