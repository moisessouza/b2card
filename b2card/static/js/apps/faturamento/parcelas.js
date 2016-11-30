"use strict";

var faturamento = angular.module('faturamento', ['commons', 'ui.bootstrap', 'ui.mask']);

faturamento.controller('FaturamentoController', function ($scope, $window){
	var $ctrl = this;
	
	$ctrl.novo = function () {
		$ctrl.parcela = {};
	}
	
	$ctrl.alertteste= function () {
		alert('Parcelas geradas');
	}
		
});
