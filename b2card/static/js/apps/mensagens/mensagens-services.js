"use strict";

var mensagens = angular.module('mensagens-services', ['ngResource']);

mensagens.config(['$resourceProvider', function($resourceProvider) {
	  // Don't strip trailing slashes from calculated URLs
	  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

mensagens.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

mensagens.service('MensagensService', function($resource){
	return {
		buscarresponsaveis: function (callback) {
			var Mensagens = $resource(BASE_URL + 'mensagens/api/responsaveis/');
			return Mensagens.query({}, callback);			
		},
		salvarresponsaveis: function (lista, callback) {
			var Mensagens = $resource(BASE_URL + 'mensagens/api/gravarresponsaveis/', {}, {
				  save: {method:'POST', isArray:true}
			 });
			return Mensagens.save({}, lista, callback);
		},
		remover: function(responsavel_id, callback) {
			var Mensagens = $resource(BASE_URL + 'mensagens/api/deletarresponsaveis/:responsavel_id/');
			return Mensagens.get({'responsavel_id':responsavel_id}, callback);
		}
	}
});
