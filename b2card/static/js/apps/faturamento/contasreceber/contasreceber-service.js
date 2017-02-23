"use strict";

var contasreceberservice = angular.module('contasreceber-service', ['ngResource']);

contasreceberservice.config(['$resourceProvider', function($resourceProvider) {
	  // Don't strip trailing slashes from calculated URLs
	  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

contasreceberservice.config(['$httpProvider', function($httpProvider) {
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

contasreceberservice.service('ContasReceberService', function($resource){
	return {
		pesquisarcontasreceber: function (args, callback){
			var Parcela = $resource(BASE_URL + 'faturamento/api/contasreceber/search/', {}, {
				'search':  {
					method:'POST',
					isArray:true
				}
			 });
			return Parcela.search({}, args, callback);
		},
		gerarpacoteitens: function (data, callback) {
			var PacoteItens = $resource(BASE_URL + 'faturamento/api/pacoteitens/');
			return PacoteItens.save({}, data,  callback);
		},
		buscarpacoteitensclienteid: function (cliente_id, callback) {
			var PacoteItens = $resource(BASE_URL + 'faturamento/api/buscarpacoteitens/:id/');
			return PacoteItens.get({'id': cliente_id}, callback);
		},
		enviarparaaprovacao: function(data, callback) {
			var PacoteItens = $resource(BASE_URL + 'faturamento/api/enviaraprovacao/');
			return PacoteItens.save(data, callback);
		},
		enviarparafaturamento: function (data, callback) {
			var PacoteItens = $resource(BASE_URL + 'faturamento/api/enviarfaturamento/');
			return PacoteItens.save(data, callback);
		}
	}
});
