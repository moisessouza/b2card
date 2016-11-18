var tipohora = angular.module('tipohora', ['tipohora-services', 'commons', 'ui.bootstrap', 'ui.mask']);

tipohora.controller('TipoHoraController', function ($scope, $window, TipoHoraService){
	var $ctrl = this;
	
	$ctrl.tipohora = {}
	
	$ctrl.show =true;
	
	$ctrl.tipohoralist = TipoHoraService.buscartipohoras();
	
	$ctrl.salvar = function () {
		TipoHoraService.salvar($ctrl.tipohora, function () {
			$ctrl.tipohoralist = TipoHoraService.buscartipohoras();
			$ctrl.tipohora = {};
		});
	}
	
	$ctrl.deletar = function (data) {
		TipoHoraService.deletar(data, function () {
			$ctrl.tipohoralist = TipoHoraService.buscartipohoras();
		});
	}
	
	$ctrl.editar = function (data) {
		$ctrl.tipohora = data;
	}
	
	$ctrl.novo = function () {
		$ctrl.tipohora = {};
	}
});