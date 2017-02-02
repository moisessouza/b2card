"use strict";

var naturezademanda = angular.module('naturezademanda', ['naturezademanda-services', 'commons', 'ui.bootstrap', 'ui.mask']);

naturezademanda.controller('NaturezaDemandaController', function ($scope, $window, NaturezaDemandaService){
	var $ctrl = this;
	
	$ctrl.naturezademanda = {}
	
	$ctrl.show =true;
	
	$ctrl.naturezademandalist = NaturezaDemandaService.buscarnaturezademandas();
	
	$ctrl.salvar = function () {
		NaturezaDemandaService.salvar($ctrl.naturezademanda, function () {
			$ctrl.naturezademandalist = NaturezaDemandaService.buscarnaturezademandas();
			$ctrl.naturezademanda = {};
		});
	}
	
	$ctrl.deletar = function (data) {
		if(confirm(MESSAGE_EXCLUIR)) {
			NaturezaDemandaService.deletar(data, function () {
				$ctrl.naturezademandalist = NaturezaDemandaService.buscarnaturezademandas();
			});
		}
	}
	
	$ctrl.editar = function (data) {
		$ctrl.naturezademanda = data;
	}
	
	$ctrl.novo = function () {
		$ctrl.naturezademanda = {};
	}
});