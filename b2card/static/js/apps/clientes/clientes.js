var clientes = angular.module('clientes', ['clientes-services', 'commons', 'ui.bootstrap']);

clientes.controller('ClientesController', function ($scope){
	var $ctrl = this;
	
	$ctrl.cliente = {
		'valorhora': []
	}
	
	$ctrl.adicionar = function () {
		$ctrl.cliente.valorhora.push({});	
	}
	
	$ctrl.deletar = function(valorhora) {
		$ctrl.cliente.valorhora.splice($ctrl.cliente.valorhora.indexOf(valorhora), 1);
	}
	
});
