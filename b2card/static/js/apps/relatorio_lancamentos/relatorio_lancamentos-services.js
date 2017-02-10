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
			var AlocacaoHoras = $resource(BASE_URL + 'relatorio_lancamentos/search/', {}, {
				'set': {method:'POST'}
			});
			return AlocacaoHoras.set({}, argumentos, callback);
		}
	}
});
