var demandas = angular.module('demandas', ['demandas-services', 'commons', 'ui.bootstrap']);

demandas.controller('DemandaController', function ($scope, $window, $uibModal, $log, DemandaService, CommonsService){
	var $ctrl = this; 
	
	var messageinfo = function (msg){
		$ctrl.clazz = 'label-primary';	
		$ctrl.message = msg;
	}

	var messagesuccess = function (msg) {
		$ctrl.clazz = 'label-success';
		$ctrl.message = msg;
	}
	
	if (demanda_id) {
		$ctrl.demanda = DemandaService.buscardemanda(demanda_id, function (data){
			$ctrl.listatipovalorhora  = DemandaService.buscartipohoracliente(cliente_id);
			$ctrl.show=true;
		});
	} else {
		$ctrl.demanda = {
			'itens_faturamento': [{}],
			'propostas':[{}],
			'tarefas':[{}],
			'observacoes':[{}]
		}
		$ctrl.show=true;
	}
	
	$ctrl.adicionaritem = function () {
		$ctrl.demanda.itens_faturamento.unshift({});
	}
	
	$ctrl.adicionarproposta = function () {
		$ctrl.demanda.propostas.unshift({});
	}
	
	$ctrl.adicionartarefa = function () {
		$ctrl.demanda.tarefas.unshift({});
	}
	
	$ctrl.adicionarobservacao = function (){
		$ctrl.demanda.observacoes.unshift({})
	}
	
	$ctrl.listaclientes= DemandaService.buscarclientes();
	$ctrl.listafuncionarios = DemandaService.buscarfuncionarios();
	
	$ctrl.changecliente = function (){
		$ctrl.listatipovalorhora  = DemandaService.buscartipohoracliente($ctrl.demanda.cliente.id);	
	}
	
	$ctrl.changehoraproposta = function (item_faturamento) {
		if (item_faturamento.tipo_hora.id){
			for (var i in $ctrl.listatipovalorhora){
				
				var tipovalorhora = $ctrl.listatipovalorhora[i]
				
				if (tipovalorhora.id == item_faturamento.tipo_hora.id){
					var tipo_hora = tipovalorhora;
					var valor_hora = parseFloat(tipo_hora.valor_hora.replace('.', '').replace(',','.'));
					item_faturamento.valor_hora = tipo_hora.valor_hora;
					var valor_faturamento = valor_hora * (item_faturamento.quantidade_horas ? item_faturamento.quantidade_horas : 0);
					item_faturamento.valor_faturamento = CommonsService.formatarnumero(valor_faturamento);
					break;
				}
			}
		}
	}
	
	
	$ctrl.salvardemanda = function (){
		messageinfo("salvando...");
		
		DemandaService.salvardemanda($ctrl.demanda, function(data){
			$ctrl.demanda = data;
			messagesuccess('salvo!')
		});
	}
	
	$ctrl.deletar = function () {
		DemandaService.deletardemanda($ctrl.demanda.id, function(data){
			$window.location.href = '/demandas/';
		});
	}
	
});