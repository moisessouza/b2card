"use strict";

var fase = angular.module('fase', ['fase-services', 'centroresultado-services', 'commons', 'ui.bootstrap', 'ui.mask']);

fase.controller('FaseController', function ($scope, $window, FaseService, CentroResultadoService){
	var $ctrl = this;
	
	$ctrl.fase = {}
	
	$ctrl.show =true;
	
	$ctrl.faselist = FaseService.buscarfases();
	$ctrl.centroresultadolist = CentroResultadoService.buscarcentroresultados();
	
	$ctrl.salvar = function () {
		FaseService.salvar($ctrl.fase, function () {
			$ctrl.faselist = FaseService.buscarfases();
			$ctrl.fase = {};
		});
	}
	
	$ctrl.deletar = function (data) {
		if(confirm(MESSAGE_EXCLUIR)) {
			FaseService.deletar(data, function () {
				$ctrl.faselist = FaseService.buscarfases();
			});
		}
	}
	
	$ctrl.editar = function (data) {
		$ctrl.fase = data;
	}
	
	$ctrl.novo = function () {
		$ctrl.fase = {};
	}
});