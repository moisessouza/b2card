var centrocusto = angular.module('centrocusto', ['centrocusto-services', 'commons', 'ui.bootstrap', 'ui.mask']);

centrocusto.controller('CentroCustoController', function ($scope, $window, CentroCustoService){
	var $ctrl = this;
	
	$ctrl.centrocusto = {}
	
	$ctrl.show =true;
	
	$ctrl.centrocustolist = CentroCustoService.buscarcentrocustos();
	
	$ctrl.salvar = function () {
		CentroCustoService.salvar($ctrl.centrocusto, function () {
			$ctrl.centrocustolist = CentroCustoService.buscarcentrocustos();
			$ctrl.centrocusto = {};
		});
	}
	
	$ctrl.deletar = function (data) {
		CentroCustoService.deletar(data, function () {
			$ctrl.centrocustolist = CentroCustoService.buscarcentrocustos();
		});
	}
	
	$ctrl.editar = function (data) {
		$ctrl.centrocusto = data;
	}
	
	$ctrl.novo = function () {
		$ctrl.centrocusto = {};
	}
	
});