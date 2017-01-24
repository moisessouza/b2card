"use strict";

var inicial = angular.module('inicial', ['inicial-services', 'commons', 'ui.bootstrap', 'ui.mask']);

inicial.controller('InicialController', function (InicialService, $scope, $window, $uibModal){
	var $ctrl = this;
	$ctrl.show=true;
	
	
	$ctrl.clientes = InicialService.buscaratividadesprofissional(function (data){
		$ctrl.clientes = data;
	});
	
});
