var clientes = angular.module('clientes', ['clientes-services', 'commons', 'ui.bootstrap']);

clientes.controller('ClientesController', function ($scope){
	var $ctrl = this;
	
	$ctrl.cliente = {
		'tipovalorhora': []
	}
	
	$ctrl.adicionar = function () {
		$ctrl.cliente.tipovalorhora.push({});	
	}
	
	$ctrl.deletar = function(tipovalorhora) {
		$ctrl.cliente.tipovalorhora.splice($ctrl.cliente.tipovalorhora.indexOf(tipovalorhora), 1);
	}
	
	$ctrl.gravar = function(){
		console.log($ctrl.cliente);
	}
	
});
