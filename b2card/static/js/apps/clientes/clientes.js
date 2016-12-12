"use strict";

var clientes = angular.module('clientes', ['clientes-services', 'centrocusto-services', 'commons', 'ui.bootstrap', 'ui.mask']);

clientes.controller('ClientesController', function ($scope, $window, ClientesService, CentroCustoService){
	var $ctrl = this;
	
	var messageinfo = function (msg){
		$ctrl.clazz = 'label-primary';	
		$ctrl.message = msg;
	}
	
	var messagesuccess = function (msg) {
		$ctrl.clazz = 'label-success';
		$ctrl.message = msg;
	}
	
	$ctrl.listacentrocusto = CentroCustoService.buscarcentrocustos();
	
	if (cliente_id) {
		$ctrl.cliente = ClientesService.buscarcliente(cliente_id, function(){
			$ctrl.show = true;
		});
	} else {
		$ctrl.cliente = {};
		$ctrl.show = true;
	}
	
	$ctrl.salvar = function(){
		messageinfo("salvando...");
		var tiposvalorhora = $ctrl.cliente.tipovalorhora
		
		for (index in tiposvalorhora){
			var tipovalor = tiposvalorhora[index];
			if (!tipovalor.tipo_hora || !tipovalor.valor_hora){
				$ctrl.cliente.tipovalorhora.splice($ctrl.cliente.tipovalorhora.indexOf(tiposvalorhora[index]), 1);
			}
		}
		
		ClientesService.salvarcliente($ctrl.cliente, function(data){
			$ctrl.cliente = data;
			messagesuccess('salvo!');
		})
	}
	
	$ctrl.deletar = function(){
		ClientesService.deletarcliente($ctrl.cliente.id, function(data){
			$window.location.href = '/clientes/';
		})
	}
	
});
