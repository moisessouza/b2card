var demandas = angular.module('demandas', ['demandas-services', 'commons', 'ui.bootstrap', 'ui.mask']);

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
	
	$ctrl.layout = function (i){
		if (i.show) {
			i.show = !i.show;
		} else {
			i.show = true;
		}
	};
	
	if (demanda_id) {
		$ctrl.demanda = DemandaService.buscardemanda(demanda_id, function (data){
			$ctrl.listatipovalorhora  = DemandaService.buscartipohoracliente(cliente_id);
			$ctrl.listacentroresultado = DemandaService.buscarcentroresultados(cliente_id);
			$ctrl.show=true;
			
			var ocorrencias = data.ocorrencias;
			for ( i in ocorrencias ){
				ocorrencias[i].show = false;
			}
			
			var tarefas = data.tarefas;
			for ( i in tarefas ){
				tarefas[i].show = false;
			}
			
		});
	} else {
		$ctrl.demanda = {
			'itens_faturamento': [{}],
			'propostas':[{}],
			'tarefas':[{}],
			'observacoes':[{}],
			'ocorrencias':[{}]
		}
		$ctrl.show=true;
	}
	
	$ctrl.adicionaritem = function () {
		$ctrl.demanda.itens_faturamento.unshift({
			'tipovalorhoras':[]
		});
	}
		
	$ctrl.adicionartipovalorhora = function (itemfaturamento) {
		if (!itemfaturamento.tipovalorhoras){
			itemfaturamento.tipovalorhoras = [];
		}
		itemfaturamento.tipovalorhoras.push({});
	}
	
	$ctrl.adicionarproposta = function () {
		$ctrl.demanda.propostas.unshift({});
	}
	
	$ctrl.adicionartarefa = function () {
		var tarefa = {'show': true};
		$ctrl.demanda.tarefas.unshift(tarefa);
	}
	
	$ctrl.adicionarobservacao = function (){
		$ctrl.demanda.observacoes.unshift({})
	}
	
	$ctrl.adicionarocorrencia = function () {
		var ocorrencia = {'show': true};
		$ctrl.demanda.ocorrencias.unshift(ocorrencia)
	}
	
	$ctrl.remover = function (i){
		i.remover = true;		
	}
	
	$ctrl.listaclientes= DemandaService.buscarclientes();
	$ctrl.listafuncionarios = DemandaService.buscarfuncionarios();
	
	$ctrl.changecliente = function (){
		$ctrl.listatipovalorhora  = DemandaService.buscartipohoracliente($ctrl.demanda.cliente.id);
		$ctrl.listacentroresultado = DemandaService.buscarcentroresultados($ctrl.demanda.cliente.id);
	}
	
	$ctrl.changedataenvioaprovacao = function (item_faturamento) {
		if (item_faturamento.data_envio_aprovacao && item_faturamento.data_envio_aprovacao.length == 10 ) {
			for (i in $ctrl.listaclientes) {
				var cliente = $ctrl.listaclientes[i];
				if (cliente.id == $ctrl.demanda.cliente.id) {
					var dias_faturamento = cliente.dias_faturamento;
					var dias_pagamento = cliente.dias_pagamento;
					var data = CommonsService.stringparadata(item_faturamento.data_envio_aprovacao);
					data.setDate(data.getDate() + dias_faturamento);
					item_faturamento.data_previsto_faturamento  = CommonsService.dataparastring(data);
					data.setDate(data.getDate() + dias_pagamento);
					item_faturamento.data_previsto_pagamento = CommonsService.dataparastring(data);
					break;
				}
			}
		}
	}
	
	$ctrl.changedataprevistofaturamento = function (item_faturamento){
		for (i in $ctrl.listaclientes) {
			var cliente = $ctrl.listaclientes[i];
			if (cliente.id == $ctrl.demanda.cliente.id) {
				var dias_pagamento = cliente.dias_pagamento;
				var data = CommonsService.stringparadata(item_faturamento.data_previsto_faturamento);
				data.setDate(data.getDate() + dias_pagamento);
				item_faturamento.data_previsto_pagamento = CommonsService.dataparastring(data);
				break;
			}
		}
	}
	
	$ctrl.recalcularfaturamentototal = function (item_faturamento) {
		if (item_faturamento.tipovalorhoras) {			
			var valortotal = 0;
			for (var i in item_faturamento.tipovalorhoras) {
				var tipovalorhora = item_faturamento.tipovalorhoras[i]
				if (!tipovalorhora.remover){
					var valor = tipovalorhora.valor_faturamento ? CommonsService.stringparafloat(tipovalorhora.valor_faturamento) : 0;
					valortotal += valor;
				}
			}
			item_faturamento.valor_total_faturamento =  CommonsService.formatarnumero(valortotal);
		}
	}
	
	$ctrl.changehoraproposta = function (tipovalorhora, item_faturamento) {
		if (tipovalorhora.tipo_hora && tipovalorhora.tipo_hora.id){
			for (var i in $ctrl.listatipovalorhora){
				
				var tipo = $ctrl.listatipovalorhora[i]
				
				if (tipo.id == tipovalorhora.tipo_hora.id){
					var tipo_hora = tipo;
					var valor_hora = CommonsService.stringparafloat(tipo_hora.valor_hora);
					tipovalorhora.valor_hora = tipo_hora.valor_hora;
					var valor_faturamento = valor_hora * (tipovalorhora.quantidade_horas ? tipovalorhora.quantidade_horas : 0);
					tipovalorhora.valor_faturamento = CommonsService.formatarnumero(valor_faturamento);
					break;
				}
			}
		}
		
		$ctrl.recalcularfaturamentototal(item_faturamento);
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