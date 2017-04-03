"use strict";

var tarefaservices = angular.module('tarefa-services', ['ngResource']);

tarefaservices.config(['$resourceProvider', function($resourceProvider) {
	  // Don't strip trailing slashes from calculated URLs
	  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

tarefaservices.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

tarefaservices.service('TarefaService', function($resource){
	return {
		buscartarefas: function (callback) {
			var Tarefa = $resource(BASE_URL + 'mensagens/tarefa/api/list/');
			return Tarefa.query(callback);
		},
		salvar: function(data, callback) {
			var Tarefa = $resource(BASE_URL + 'mensagens/tarefa/api/detail/');
			return Tarefa.save(data, callback);
		},
		deletar: function(data, callback){
			var Tarefa = $resource(BASE_URL + 'mensagens/tarefa/api/:id/');
			return Tarefa.remove({id: data.id}, data, callback);
		}
	}
});
