"use strict";

var valorhoraservice = angular.module('valorhora-services', ['ngResource']);

valorhoraservice.config(['$resourceProvider', function($resourceProvider) {
	  // Don't strip trailing slashes from calculated URLs
	  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

valorhoraservice.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

valorhoraservice.service('ValorHoraService', function($resource){
	return {
		buscarvalorhora: function (valor_hora_id, callback){
			var ValorHora = $resource(BASE_URL + 'cadastros/valorhora/api/:id/');
			return ValorHora.get({id: valor_hora_id}, callback);
		},
		salvar: function (data, callback) {
			var ValorHora = $resource(BASE_URL + 'cadastros/valorhora/api/detail/');
			return ValorHora.save(data, callback);
		},
		deletar: function (valor_hora_id, callback) {
			var ValorHora = $resource(BASE_URL + 'cadastros/valorhora/api/:id/');
			return ValorHora.remove({id: valor_hora_id}, callback)
		},
		buscarvalorhoraporcliente: function (cliente_id, callback) {
			var ValorHora = $resource(BASE_URL + 'cadastros/valorhora/api/cliente/:id/');
			return ValorHora.query({id: cliente_id}, callback)
		},
		buscarvalorhorab2card: function(callback) {
			var CentroCusto = $resource(BASE_URL + 'cadastros/valorhora/api/b2card/');
			return CentroCusto.query(callback);
		},
	}
});
