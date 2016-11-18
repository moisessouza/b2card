var naturezaoperacaoservices = angular.module('naturezaoperacao-services', ['ngResource']);

naturezaoperacaoservices.config(['$resourceProvider', function($resourceProvider) {
	  // Don't strip trailing slashes from calculated URLs
	  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

naturezaoperacaoservices.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

naturezaoperacaoservices.service('NaturezaOperacaoService', function($resource){
	return {
		buscarnaturezaoperacoes: function (callback) {
			var NaturezaOperacao = $resource('/cadastros/naturezaoperacao/api/list/');
			return NaturezaOperacao.query(callback);
		},
		salvar: function(data, callback) {
			var NaturezaOperacao = $resource('/cadastros/naturezaoperacao/api/detail/');
			return NaturezaOperacao.save(data, callback);
		},
		deletar: function(data, callback){
			var NaturezaOperacao = $resource('/cadastros/naturezaoperacao/api/:id/');
			return NaturezaOperacao.remove({id: data.id}, data, callback);
		}
	}
});
