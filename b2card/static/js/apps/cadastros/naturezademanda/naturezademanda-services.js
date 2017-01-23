"use strict";

var naturezademandaservices = angular.module('naturezademanda-services', ['ngResource']);

naturezademandaservices.config(['$resourceProvider', function($resourceProvider) {
	  // Don't strip trailing slashes from calculated URLs
	  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

naturezademandaservices.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

naturezademandaservices.service('NaturezaDemandaService', function($resource){
	return {
		buscarnaturezademandas: function (callback) {
			var NaturezaDemanda = $resource(BASE_URL + 'cadastros/naturezademanda/api/list/');
			return NaturezaDemanda.query(callback);
		},
		salvar: function(data, callback) {
			var NaturezaDemanda = $resource(BASE_URL + 'cadastros/naturezademanda/api/detail/');
			return NaturezaDemanda.save(data, callback);
		},
		deletar: function(data, callback){
			var NaturezaDemanda = $resource(BASE_URL + 'cadastros/naturezademanda/api/:id/');
			return NaturezaDemanda.remove({id: data.id}, data, callback);
		}
	}
});
