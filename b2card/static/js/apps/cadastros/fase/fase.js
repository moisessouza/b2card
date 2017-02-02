"use strict";

var fase = angular.module('fase', ['fase-services', 'commons', 'ui.bootstrap', 'ui.mask']);

fase.controller('FaseController', function ($scope, $window, FaseService){
	var $ctrl = this;
	
	$ctrl.fase = {}
	
	$ctrl.show =true;
	
	$ctrl.faselist = FaseService.buscarfases();
	
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