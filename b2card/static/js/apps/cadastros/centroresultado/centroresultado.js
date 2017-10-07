"use strict";

var centroresultado = angular.module('centroresultado', ['centroresultado-services', 'commons', 'ui.bootstrap', 'ui.mask']);

centroresultado.controller('CentroResultadoController', function ($scope, $window, CentroResultadoService){
	var $ctrl = this;
	
	$ctrl.centroresultado = {}
	
	$ctrl.show =true;
	
	$ctrl.centroresultadolist = CentroResultadoService.buscarcentroresultados();
	
	$ctrl.salvar = function () {
		CentroResultadoService.salvar($ctrl.centroresultado, function () {
			$ctrl.centroresultadolist = CentroResultadoService.buscarcentroresultados();
			$ctrl.centroresultado = {};
		});
	}
	
	$ctrl.deletar = function (data) {
		if(confirm(MESSAGE_EXCLUIR)) {
			CentroResultadoService.deletar(data, function () {
				$ctrl.centroresultadolist = CentroResultadoService.buscarcentroresultados();
			});
		}
	}
	
	
	$ctrl.editar = function (data) {
		$ctrl.centroresultado = data;
	}
	
	$ctrl.novo = function () {
		$ctrl.centroresultado = {};
	}
	
});