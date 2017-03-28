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
		validardatahora: function(data, hora_inicio, hora_fim, callback) {
			var CustoPrestador = $resource(BASE_URL + 'inicial/api/validar_data_hora/:data_informada/:hora_inicio/:hora_fim/');
			return CustoPrestador.get({'data_informada': data, 'hora_inicio': hora_inicio, 'hora_fim': hora_fim}, callback);
		},
		salvarlotedespesa: function(data, callback) {
			var LoteDespesa = $resource(BASE_URL + 'faturamento/api/lotedespesas/new/');
			return LoteDespesa.save({}, data, callback);
		},
		buscarlotesemaberto: function(demanda_id, callback) {
			var LoteDespesa = $resource(BASE_URL + 'faturamento/api/lotedespesas/abertos/:demanda_id/');
			return LoteDespesa.query({'demanda_id':demanda_id}, callback);
		},
		buscarresumododia: function(data, callback){
			var AlocacaoHoras = $resource(BASE_URL + 'inicial/api/total_horas_lancadas_dia/:data_informada/');
			return AlocacaoHoras.get({'data_informada': data}, callback)
		},
		buscarmensagensusuario: function (callback) {
			var Mensagens = $resource(BASE_URL + 'mensagens/api/list');
			return Mensagens.query({}, callback);
		},
		marcarmensagemcomolido: function(mensagem_id, callback){
			var Mensagens = $resource(BASE_URL + 'mensagens/api/marcarcomolido/:mensagem_id/');
			return Mensagens.get({'mensagem_id':mensagem_id}, callback);
		}
	}
});
