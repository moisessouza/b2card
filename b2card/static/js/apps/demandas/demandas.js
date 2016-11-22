"use strict";

var demandas = angular.module('demandas', ['demandas-services', 'centrocusto-services', 'valorhora-services', 
                                           'centroresultado-services', 'commons', 'ui.bootstrap', 'ui.mask']);

demandas.controller('DemandaController', function ($scope, $window, $uibModal, $log, DemandaService, 
		CentroCustoService, ValorHoraService, CommonsService, CentroResultadoService){
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
	
	var configurarorcamento = function (data) {
		if (data.orcamento){
			
			var idcentrocusto = data.orcamento.centro_custo.id;
			$ctrl.listavalorhora = ValorHoraService.buscarvalorhoraporcentrodecusto(idcentrocusto);
			
			data.orcamento.total_orcamento = CommonsService.formatarnumero(data.orcamento.total_orcamento);
			
			if (data.orcamento.fases) {
				
				for (var i in data.orcamento.fases){
					
					var fase =  data.orcamento.fases[i]
					fase.valor_total = CommonsService.formatarnumero(fase.valor_total);
					
					if (fase.itensfase) {
						for (var j in fase.itensfase) {
							var itemfase = fase.itensfase[j]
							itemfase.valor_selecionado = CommonsService.formatarnumero(itemfase.valor_selecionado);
							itemfase.valor_total = CommonsService.formatarnumero(itemfase.valor_total);
						}
					}
				}
			}				
		}
	}
	
	$ctrl.changeatividade = function () {
		
		var tipos_centro_resultado = {}
		
		for (var int = 0; int < $ctrl.demanda.atividades.length; int++) {
			var atividade = $ctrl.demanda.atividades[int];
			
			if (!atividade.remover){
			
				var id_centro_resultado = atividade.centro_resultado.id;
				var horas_previstas = atividade.horas_previstas;
				
				if (tipos_centro_resultado[id_centro_resultado]){
					tipos_centro_resultado[id_centro_resultado]+=horas_previstas;
				} else {
					tipos_centro_resultado[id_centro_resultado]=horas_previstas;
				}
			
			}
		}	
		
		for(var int = 0; int < $ctrl.listacentroresultadoshoras.length; int++){
		
			var tipo_resultado_horas = $ctrl.listacentroresultadoshoras[int];
			tipo_resultado_horas.horas_restantes = tipo_resultado_horas.total_horas;
			
			for (var id_tipo in tipos_centro_resultado){
				
				var horas_gastas = tipos_centro_resultado[id_tipo];

				if (horas_gastas && tipo_resultado_horas.fase__itemfase__valor_hora__centro_resultado__id == id_tipo){
					tipo_resultado_horas.horas_restantes = tipo_resultado_horas.total_horas - horas_gastas;
				}
			}
		}
		
	}
	
	if (demanda_id) {
		$ctrl.demanda = DemandaService.buscardemanda(demanda_id, function (data){
			
			console.log(data);
			
			$ctrl.listatipovalorhora  = DemandaService.buscartipohoracliente(cliente_id);
			$ctrl.listacentroresultado = DemandaService.buscarcentroresultados(cliente_id);
			$ctrl.show=true;
			
			var ocorrencias = data.ocorrencias;
			for ( var i in ocorrencias ){
				ocorrencias[i].show = false;
			}
			
			var tarefas = data.tarefas;
			for ( var i in tarefas ){
				tarefas[i].show = false;
			}
			
			configurarorcamento(data);
			
			$ctrl.listacentroresultadoshoras = DemandaService.buscarcentroresultadoshora(demanda_id, $ctrl.changeatividade);
			
		});
		
	} else {
		$ctrl.demanda = {
			'itens_faturamento': [{}],
			'propostas':[{}],
			'tarefas':[{}],
			'observacoes':[{}],
			'ocorrencias':[{}],
			'orcamento': {},
			'atividades': [{}]
		}
		$ctrl.show=true;
		$ctrl.listacentroresultadoshoras = []
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
		$ctrl.demanda.ocorrencias.unshift(ocorrencia);
	}
	
	$ctrl.adicionarfase = function () {
		if (!$ctrl.demanda.orcamento){
			$ctrl.demanda.orcamento = {}
		}
		if (!$ctrl.demanda.orcamento.fases){
			$ctrl.demanda.orcamento.fases = [];
		}
		$ctrl.demanda.orcamento.fases.push({})
	}
	
	$ctrl.adicionaritemfase = function (fase){
		if (!fase.itensfase){
			fase.itensfase = [];
		}
		fase.itensfase.push({});
	}
		
	$ctrl.adicionaritemfase = function (fase){
		if (!fase.itensfase){
			fase.itensfase = [];
		}
		fase.itensfase.push({});
	}
	
	$ctrl.adicionaratividade = function () {
		if(!$ctrl.demanda.atividades){
			$ctrl.demanda.atividades = [];
		}
		
		$ctrl.demanda.atividades.unshift({});
		
	}
	
	$ctrl.remover = function (i, callback){
		i.remover = true;		
		if (callback){
			callback();
		}
	}
		
	$ctrl.listaclientes= DemandaService.buscarclientes();
	$ctrl.listafuncionarios = DemandaService.buscarfuncionarios();
	$ctrl.listacentrocustos = CentroCustoService.buscarcentrocustos();
	$ctrl.listacentroresultados = CentroResultadoService.buscarcentroresultados();
	
	$ctrl.changecentrocusto = function () {
		var idcentrocusto = $ctrl.demanda.orcamento.centro_custo.id;
		$ctrl.listavalorhora = ValorHoraService.buscarvalorhoraporcentrodecusto(idcentrocusto);
	}
	
	$ctrl.changevalorhora = function (itemfase) {
		itemfase.valor_selecionado = CommonsService.formatarnumero(0);
		for (var i in $ctrl.listavalorhora){
			var valorhora = $ctrl.listavalorhora[i]
			if (valorhora && valorhora.vigencia){
				if (valorhora.id == itemfase.valor_hora.id){
					itemfase.valor_selecionado = CommonsService.formatarnumero(valorhora.vigencia && valorhora.vigencia.valor ? valorhora.vigencia.valor : 0);
					break;
				}
			}
		}
		$ctrl.changefasequantidadehoras(itemfase);
	}
	
	$ctrl.calcularvalortotalorcamento = function (){
		
		var fases = $ctrl.demanda.orcamento.fases;
		var totalorcamento = 0;
		
		for (var i in fases) {
			var fase = fases[i];
			if (!fase.remover) {
				var itensfase = fase.itensfase;
				
				var valorfase = 0
				for (i in itensfase){
					var itemfase = itensfase[i];
					if (!itemfase.remover && itemfase.valor_total) {
						var valoritem = CommonsService.stringparafloat(itemfase.valor_total);
						valorfase+=valoritem;
					}
				}
				
				fase.valor_total = CommonsService.formatarnumero(valorfase);
				totalorcamento+= valorfase;
			}
		}
		
		$ctrl.demanda.orcamento.total_orcamento =  CommonsService.formatarnumero(totalorcamento);
	}
	
	$ctrl.changefasequantidadehoras = function (itemfase) {
		for (var i in $ctrl.listavalorhora){
			var valorhora = $ctrl.listavalorhora[i]
			if (valorhora.id == itemfase.valor_hora.id){
				itemfase.valor_total  = CommonsService.formatarnumero((valorhora.vigencia ? valorhora.vigencia.valor : 0) * ( itemfase.quantidade_horas ? itemfase.quantidade_horas : 0));
			}
		}
		
		$ctrl.calcularvalortotalorcamento();
		
	}
	
	$ctrl.changecliente = function (){
		$ctrl.listatipovalorhora  = DemandaService.buscartipohoracliente($ctrl.demanda.cliente.id);
		$ctrl.listacentroresultado = DemandaService.buscarcentroresultados($ctrl.demanda.cliente.id);
	}
	
	$ctrl.changedataenvioaprovacao = function (item_faturamento) {
		if (item_faturamento.data_envio_aprovacao && item_faturamento.data_envio_aprovacao.length == 10 ) {
			for (var i in $ctrl.listaclientes) {
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
		for (var i in $ctrl.listaclientes) {
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
			configurarorcamento(data);
			$ctrl.listacentroresultadoshoras = DemandaService.buscarcentroresultadoshora(demanda_id, $ctrl.changeatividade);
			messagesuccess('salvo!')
		});
	}
	
	$ctrl.deletar = function () {
		DemandaService.deletardemanda($ctrl.demanda.id, function(data){
			$window.location.href = '/demandas/';
		});
	}
	
});