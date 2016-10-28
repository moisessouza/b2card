var produtosservices = angular.module('produtos-services', ['ngResource']);

produtosservices.config(['$resourceProvider', function($resourceProvider) {
	  // Don't strip trailing slashes from calculated URLs
	  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

produtosservices.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

produtosservices.service('MateriaisService', function ($resource) {
	return {
		buscarmateriais:function () {
			var Materiais = $resource('/materiais/api/list/');
			var result = Materiais.query();
			console.log(result)
			return result;
		}
	}
	
}).service('ProdutoService', function ($resource){
	return {
		buscarproduto: function (id, callback) {
			var Produto = $resource('/produtos/api/:id');
			var result = Produto.get({'id': id}, function (data) {
				if (callback) {
					callback(data);
				}
			});
			return result;
		},
		salvarproduto: function (data, callback) {
			var Produto = $resource('/produtos/api/save/');
			var result = Produto.save(data, function (data) {
				if (callback){
					callback(data);
				}
			});
			return result;
		},
		buscartodosprodutos: function(callback){
			var Produto = $resource('/produtos/api/list/')
			var result = Produto.query(callback);
			return result;
		}
	}
});