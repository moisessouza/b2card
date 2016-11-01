var clientes = angular.module('clientes', ['clientes-services', 'commons', 'ui.bootstrap']);

clientes.controller('ClientesController', function ($scope, $window, ClientesService){
	var $ctrl = this;
	
	var messageinfo = function (msg){
		$ctrl.clazz = 'label-primary';	
		$ctrl.message = msg;
	}
	
	var messagesuccess = function (msg) {
		$ctrl.clazz = 'label-success';
		$ctrl.message = msg;
	}
	
	if (cliente_id) {
		$ctrl.cliente = ClientesService.buscarcliente(cliente_id);
	} else {
		$ctrl.cliente = {
			'tipovalorhora': []
		}
	}
	
	$ctrl.adicionar = function () {
		$ctrl.cliente.tipovalorhora.push({
			'tipo_hora': null,
			'valor_hora': null
		});	
	}
	
	$ctrl.deletarvalorhora = function(tipovalorhora) {
		if (tipovalorhora.id){
			var confirm = $window.confirm("Tem certeza que deseja deletar esse funcionário?");
			if (confirm){
				ClientesService.deletartipovalorhora(tipovalorhora.id, function (data){
					$ctrl.cliente.tipovalorhora.splice($ctrl.cliente.tipovalorhora.indexOf(tipovalorhora), 1);
				});
			}
		} else {
			$ctrl.cliente.tipovalorhora.splice($ctrl.cliente.tipovalorhora.indexOf(tipovalorhora), 1);
		}
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
