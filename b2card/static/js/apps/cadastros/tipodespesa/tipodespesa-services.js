"use strict";

var tipodespesaservices = angular.module('tipodespesa-services', ['ngResource']);

tipodespesaservices.config(['$resourceProvider', function($resourceProvider) {
	  // Don't strip trailing slashes from calculated URLs
	  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

tipodespesaservices.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

tipodespesaservices.service('TipoDespesaService', function($resource){
	return {
		buscartipodespesas: function (callback) {
			var TipoDespesa = $resource(BASE_URL + 'cadastros/tipodespesa/api/list/');
			return TipoDespesa.query(callback);
		},
		salvar: function(data, callback) {
			var TipoDespesa = $resource(BASE_URL + 'cadastros/tipodespesa/api/detail/');
			return TipoDespesa.save(data, callback);
		},
		deletar: function(data, callback){
			var TipoDespesa = $resource(BASE_URL + 'cadastros/tipodespesa/api/:id/');
			return TipoDespesa.remove({id: data.id}, data, callback);
		}
	}
});
