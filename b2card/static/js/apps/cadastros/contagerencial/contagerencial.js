var contagerencial = angular.module('contagerencial', ['contagerencial-services', 'commons', 'ui.bootstrap', 'ui.mask']);

contagerencial.controller('ContaGerencialController', function ($scope, $window, ContaGerencialService){
	var $ctrl = this;
	
	$ctrl.contagerencial = {}
	
	$ctrl.show =true;
	
	$ctrl.contagerenciallist = ContaGerencialService.buscarcontagerenciais();
	
	$ctrl.salvar = function () {
		ContaGerencialService.salvar($ctrl.contagerencial, function () {
			$ctrl.contagerenciallist = ContaGerencialService.buscarcontagerenciais();
			$ctrl.contagerencial = {};
		});
	}
	
	$ctrl.deletar = function (data) {
		ContaGerencialService.deletar(data, function () {
			$ctrl.contagerenciallist = ContaGerencialService.buscarcontagerenciais();
		});
	}
	
	$ctrl.editar = function (data) {
		$ctrl.contagerencial = data;
	}
	
	$ctrl.novo = function () {
		$ctrl.contagerencial = {};
	}
	
});