"use strict";

var recursosservices = angular.module('recursos-services', ['ngResource']);

recursosservices.config(['$resourceProvider', function($resourceProvider) {
	  // Don't strip trailing slashes from calculated URLs
	  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

recursosservices.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

recursosservices.service('RecursosService', function($resource){
	return {
		buscarcargos: function (callback) {
			var Cargo = $resource('/recursos/api/cargo/list/');
			return Cargo.query(callback);
		},
		salvarcargo: function (cargo, callback) {
			var Cargo = $resource('/recursos/api/cargo/new/');
			Cargo.save(cargo, callback);
		},
		deletarcargo: function (cargo, callback) {
			var Cargo = $resource('/recursos/api/cargo/:id/')
			return Cargo.remove({'id':cargo.id}, callback);
		},
		buscarusuariosnaousados: function (callback) {
			var Usuarios = $resource('/recursos/api/usuarios/');
			return Usuarios.query(callback);
		}, 
		buscarusuarioprestador: function (id_prestador, callback) {
			var Usuarios = $resource('/recursos/api/usuarios/:id');
			return Usuarios.query({id:id_prestador}, callback)
		},
		salvarfuncionario: function (funcionario, callback) {
			var Funcionario = $resource('/recursos/api/new/');
			Funcionario.save(funcionario, callback);
		},
		buscarfuncionario: function (id, callback) {
			var Funcionario = $resource('/recursos/api/:id/');
			return Funcionario.get({'id':id}, callback);
		},
		deletarfuncionario: function (id, callback) {
			var Funcionario = $resource('/recursos/api/:id/');
			return Funcionario.remove({'id':id}, callback);
		}
	}
});
