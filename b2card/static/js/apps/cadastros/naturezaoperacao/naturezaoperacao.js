"use strict";

var naturezaoperacao = angular.module('naturezaoperacao', ['naturezaoperacao-services', 'commons', 'ui.bootstrap', 'ui.mask']);

naturezaoperacao.controller('NaturezaOperacaoController', function ($scope, $window, NaturezaOperacaoService){
	var $ctrl = this;
	
	$ctrl.naturezaoperacao = {}
	
	$ctrl.show =true;
	
	$ctrl.naturezaoperacaolist = NaturezaOperacaoService.buscarnaturezaoperacoes();
	
	$ctrl.salvar = function () {
		NaturezaOperacaoService.salvar($ctrl.naturezaoperacao, function () {
			$ctrl.naturezaoperacaolist = NaturezaOperacaoService.buscarnaturezaoperacoes();
			$ctrl.naturezaoperacao = {};
		});
	}
	
	$ctrl.deletar = function (data) {
		NaturezaOperacaoService.deletar(data, function () {
			$ctrl.naturezaoperacaolist = NaturezaOperacaoService.buscarnaturezaoperacoes();
		});
	}
	
	$ctrl.editar = function (data) {
		$ctrl.naturezaoperacao = data;
	}
	
	$ctrl.novo = function () {
		$ctrl.naturezaoperacao = {};
	}
	
});