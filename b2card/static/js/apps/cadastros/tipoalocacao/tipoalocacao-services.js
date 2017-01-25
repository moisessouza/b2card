"use strict";

var tipoalocacaoservices = angular.module('tipoalocacao-services', ['ngResource']);

tipoalocacaoservices.config(['$resourceProvider', function($resourceProvider) {
	  // Don't strip trailing slashes from calculated URLs
	  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

tipoalocacaoservices.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

tipoalocacaoservices.service('TipoAlocacaoService', function($resource){
	return {
		buscartipoalocacoes: function (callback) {
			var TipoAlocacao = $resource(BASE_URL + 'cadastros/tipoalocacao/api/list/');
			return TipoAlocacao.query(callback);
		},
		salvar: function(data, callback) {
			var TipoAlocacao = $resource(BASE_URL + 'cadastros/tipoalocacao/api/detail/');
			return TipoAlocacao.save(data, callback);
		},
		deletar: function(data, callback){
			var TipoAlocacao = $resource(BASE_URL + 'cadastros/tipoalocacao/api/:id/');
			return TipoAlocacao.remove({id: data.id}, data, callback);
		}
	}
});
