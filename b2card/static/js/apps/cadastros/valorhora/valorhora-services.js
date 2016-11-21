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
			var ValorHora = $resource('/cadastros/valorhora/api/:id/');
			return ValorHora.get({id: valor_hora_id}, callback);
		},
		salvar: function (data, callback) {
			var ValorHora = $resource('/cadastros/valorhora/api/detail/');
			return ValorHora.save(data, callback);
		},
		deletar: function (valor_hora_id, callback) {
			var ValorHora = $resource('/cadastros/valorhora/api/:id/');
			return ValorHora.remove({id: valor_hora_id}, callback)
		},
		buscarvalorhoraporcentrodecusto: function (centro_custo_id, callback) {
			var ValorHora = $resource('/cadastros/valorhora/api/centrocusto/:id/');
			return ValorHora.query({id: centro_custo_id}, callback)
		}
	}
});
