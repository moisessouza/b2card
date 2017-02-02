"use strict";

var centrocusto = angular.module('unidadeadministrativa', ['unidadeadministrativa-services', 'commons', 'ui.bootstrap', 'ui.mask']);

centrocusto.controller('UnidadeAdministrativaController', function ($scope, $window, UnidadeAdministrativaService){
	var $ctrl = this;
	
	$ctrl.unidadeadministrativa = {}
	
	$ctrl.show =true;
	
	$ctrl.unidadeadministrativalist = UnidadeAdministrativaService.buscarunidadeadministrativas();
	
	$ctrl.salvar = function () {
		UnidadeAdministrativaService.salvar($ctrl.unidadeadministrativa, function () {
			$ctrl.unidadeadministrativalist = UnidadeAdministrativaService.buscarunidadeadministrativas();
			$ctrl.unidadeadministrativa = {};
		});
	}
	
	$ctrl.deletar = function (data) {
		if(confirm(MESSAGE_EXCLUIR)) {
			UnidadeAdministrativaService.deletar(data, function () {
				$ctrl.unidadeadministrativalist = UnidadeAdministrativaService.buscarunidadeadministrativas();
			});
		}
	}
	
	$ctrl.editar = function (data) {
		$ctrl.unidadeadministrativa = data;
	}
	
	$ctrl.novo = function () {
		$ctrl.unidadeadministrativa = {};
	}
	
});