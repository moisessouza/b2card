"use strict";

var tipoalocacao = angular.module('tipoalocacao', ['tipoalocacao-services', 'commons', 'ui.bootstrap', 'ui.mask']);

tipoalocacao.controller('TipoAlocacaoController', function ($scope, $window, TipoAlocacaoService){
	var $ctrl = this;
	
	$ctrl.tipoalocacao = {}
	
	$ctrl.show =true;
	
	$ctrl.tipoalocacaolist = TipoAlocacaoService.buscartipoalocacoes();
	
	$ctrl.salvar = function () {
		TipoAlocacaoService.salvar($ctrl.tipoalocacao, function () {
			$ctrl.tipoalocacaolist = TipoAlocacaoService.buscartipoalocacoes();
			$ctrl.tipoalocacao = {};
		});
	}
	
	$ctrl.deletar = function (data) {
		TipoAlocacaoService.deletar(data, function () {
			$ctrl.tipoalocacaolist = TipoAlocacaoService.buscartipoalocacoes();
		});
	}
	
	$ctrl.editar = function (data) {
		$ctrl.tipoalocacao = data;
	}
	
	$ctrl.novo = function () {
		$ctrl.tipoalocacao = {};
	}
});