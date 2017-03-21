"use strict";

var tipodespesa = angular.module('tipodespesa', ['tipodespesa-services', 'commons', 'ui.bootstrap', 'ui.mask']);

tipodespesa.controller('TipoDespesaController', function ($scope, $window, TipoDespesaService){
	var $ctrl = this;
	
	$ctrl.tipodespesa = {}
	
	$ctrl.show =true;
	
	$ctrl.tipodespesalist = TipoDespesaService.buscartipodespesas();
	
	$ctrl.salvar = function () {
		TipoDespesaService.salvar($ctrl.tipodespesa, function () {
			$ctrl.tipodespesalist = TipoDespesaService.buscartipodespesas();
			$ctrl.tipodespesa = {};
		});
	}
	
	$ctrl.deletar = function (data) {
		if(confirm(MESSAGE_EXCLUIR)) {
			TipoDespesaService.deletar(data, function () {
				$ctrl.tipodespesalist = TipoDespesaService.buscartipodespesas();
			});
		}
	}
	
	$ctrl.editar = function (data) {
		$ctrl.tipodespesa = data;
	}
	
	$ctrl.novo = function () {
		$ctrl.tipodespesa = {};
	}
});