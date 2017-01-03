"use strict";

var demandas = angular.module('demandas', ['demandas-services', 'centrocusto-services', 'valorhora-services', 'parcela', 'parcela-services',
                                           'centroresultado-services', 'unidadeadministrativa-services', 'commons', 'ui.bootstrap', 'ui.mask']);

demandas.factory('share', function(){
	  return {};
});

demandas.controller('DemandaController', function ($scope, $window, $uibModal, $log, DemandaService, ParcelaService,
		CentroCustoService, ValorHoraService, CommonsService, CentroResultadoService, UnidadeAdministrativaService, share, MessageService){
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
	
	$ctrl.atividade = {};
	
	var configuraritensfaturamento = function (data) {
		if (data.itens_faturamento) {
			for (var i in data.itens_faturamento) {
				var valorhoras = data.itens_faturamento[i].valorhoras
				if (valorhoras){
					for (var v in valorhoras) {
						var valorhora = valorhoras[v]
						valorhora.valor = CommonsService.formatarnumero(valorhora.valor);
					}
				}
			}
		}
	}
	
	var configurarorcamento = function (data) {
		
		if (data.cliente){
			$ctrl.listavalorhora = ValorHoraService.buscarvalorhoraporcliente(data.cliente.id);
		}
		
		if (data.orcamento){
			
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
	
	$ctrl.changecliente = function () {
		if ($ctrl.demanda.cliente){
			$ctrl.listavalorhora = ValorHoraService.buscarvalorhoraporcliente($ctrl.demanda.cliente.id);
		}
	}
	
	$ctrl.modalprevisaofaturamento = function (){
		var modalInstance = $uibModal.open({
			animation : $ctrl.animationsEnabled,
			ariaLabelledBy : 'modal-title',
			ariaDescribedBy : 'modal-body',
			templateUrl : '/static/modal/modalContasReceber.html?bust=' + Math.random().toString(36).slice(2),
			controller : 'ModalParcelasController',
			controllerAs : '$ctrl',
			//size : 'lg'
			windowClass: 'app-modal-window',
			resolve : {
				demanda : function() {
					return $ctrl.demanda;
				},
				listavalorhora: function () {
					return $ctrl.listavalorhora;
				}
				
			}
		});
			
		modalInstance.result.then(function(data) {
			configurardemanda($ctrl.demanda.id);
		}, function() {
			// $log.info('Modal dismissed at: ' + new Date());
		});
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
	
	var configurardemanda = function (demanda_id) {
	
		if (demanda_id) {
			$ctrl.demanda = DemandaService.buscardemanda(demanda_id, function (data){
				
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
				configuraritensfaturamento(data);
				//configurarparcelas(data);
				
				/*ParcelaService.buscartotalhoras(data.id, function (data){
					$ctrl.parcela.total_horas = data.total_horas
					$ctrl.calcularvalorrestante();
				});
				
				ParcelaService.buscartotalhorasporvalorhora(data.id, function(data){
					$ctrl.valorhoras_horas_raw = data;
					
					for (var i = 0; i < $ctrl.valorhoras_horas_raw.length; i++){
						$ctrl.valorhoras_horas_raw[i].horas_restantes = $ctrl.valorhoras_horas_raw[i].total_horas;
					}
					
					$ctrl.calcularhorasrestantesparcela();
				});*/
				
				
				$ctrl.listacentroresultadoshoras = DemandaService.buscarcentroresultadoshora(demanda_id, $ctrl.changeatividade);
				
			});
			
			share.demanda = $ctrl.demanda;
			
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
	
	}
	
	configurardemanda(demanda_id);
	
	$ctrl.adicionaritem = function () {
		$ctrl.demanda.itens_faturamento.unshift({
			'valorhoras':[]
		});
	}
		
	$ctrl.adicionarvalorhora = function (itemfaturamento) {
		if (!itemfaturamento.valorhoras){
			itemfaturamento.valorhoras = [];
		}
		itemfaturamento.valorhoras.push({});
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
	
	$ctrl.novafase = function () {
		$ctrl.fase = {
			itensfase: [{}]
		};
	}
	
	$ctrl.cancelarfase = function () {
		$ctrl.fase = null;
	}
	
	$ctrl.editarfase = function (fase) {
		$ctrl.fase = fase;
	}
	
	$ctrl.salvarfase = function () {
		if (!$ctrl.demanda.orcamento){
			$ctrl.demanda.orcamento = {};
		}
		if (!$ctrl.demanda.orcamento.fases){
			$ctrl.demanda.orcamento.fases = [];
		}
		
		if ($ctrl.fase.descricao){
			
			if ( $ctrl.fase.itensfase){
				for (var i in $ctrl.fase.itensfase){
					var itemfase = $ctrl.fase.itensfase[i];
					for (var j in $ctrl.listavalorhora){
				
						var valorhora = $ctrl.listavalorhora[j];
						if (itemfase.valor_hora && valorhora.id == itemfase.valor_hora.id){
							itemfase.valor_hora.descricao = valorhora.descricao;
							break;
						}
					}
					
				}
			}
			
			if ($ctrl.demanda.orcamento.fases.indexOf($ctrl.fase) < 0){
				$ctrl.demanda.orcamento.fases.push($ctrl.fase);	
			}
		}
		
		$ctrl.fase = null;
		
		$ctrl.calcularvalortotalorcamento();
	}
	
	$ctrl.adicionaritemfase = function (){
		if (!$ctrl.fase.itensfase){
			$ctrl.fase.itensfase = [];
		}
		$ctrl.fase.itensfase.push({});
	}
	
	$ctrl.novaatividade = function () {
		$ctrl.atividade = {};
	}
	
	$ctrl.salvaratividade = function () {
		if(!$ctrl.demanda.atividades){
			$ctrl.demanda.atividades = [];
		}
		
		if ($ctrl.demanda.atividades.indexOf($ctrl.atividade) < 0){
			$ctrl.demanda.atividades.push($ctrl.atividade);	
		}
		
		for (var i in $ctrl.listafuncionarios){
			var funcionario = $ctrl.listafuncionarios[i];
			if (funcionario.id == $ctrl.atividade.responsavel.id){
				$ctrl.atividade.responsavel.nome = funcionario.nome;
			}
		}
		
		$ctrl.changeatividade();
		
		$ctrl.atividade = {};
		
	}
	
	$ctrl.editaratividade = function (atividade) {
		$ctrl.atividade = atividade;
	}
	
	$ctrl.remover = function (i, callback){
		i.remover = true;		
		if (callback){
			callback();
		}
	}
		
	$ctrl.listaclientes= DemandaService.buscarclientes();
	$ctrl.listafuncionarios = DemandaService.buscarfuncionarios();
	$ctrl.listacentroresultados = CentroResultadoService.buscarcentroresultados();
	$ctrl.listaunidadeadministrativas = UnidadeAdministrativaService.buscarunidadeadministrativas();
	
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
		
		var itensfase = $ctrl.fase.itensfase;
		
		var valorfase = 0
		for (i in itensfase){
			var itemfase = itensfase[i];
			if (!itemfase.remover && itemfase.valor_total) {
				var valoritem = CommonsService.stringparafloat(itemfase.valor_total);
				valorfase+=valoritem;
			}
		}
		
		$ctrl.fase.valor_total = CommonsService.formatarnumero(valorfase);
		
		$ctrl.calcularvalortotalorcamento();
		
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
		if (item_faturamento.valorhoras) {			
			var valortotal = 0;
			for (var i in item_faturamento.valorhoras) {
				var valorhora = item_faturamento.valorhoras[i]
				if (!valorhora.remover){
					var valor = valorhora.valor_faturamento ? CommonsService.stringparafloat(valorhora.valor_faturamento) : 0;
					valortotal += valor;
				}
			}
			item_faturamento.valor_total_faturamento =  CommonsService.formatarnumero(valortotal);
		}
	}
	
	$ctrl.changevalorhoraitem = function (valorhora, item_faturamento) {
		if (valorhora.valor_hora && valorhora.valor_hora.id){
			for (var i in $ctrl.listavalorhora){
				
				var valor = $ctrl.listavalorhora[i]
				
				if (valor.id == valorhora.valor_hora.id){
					var valor_hora = valor.vigencia.valor;
					valorhora.valor = CommonsService.formatarnumero(valor_hora);
					var valor_faturamento = valor_hora * (valorhora.quantidade_horas ? valorhora.quantidade_horas : 0);
					valorhora.valor_faturamento = CommonsService.formatarnumero(valor_faturamento);
					break;
				}
			}
		}
		
		$ctrl.recalcularfaturamentototal(item_faturamento);
	}
	
	
	$ctrl.salvardemanda = function (){
		MessageService.messageinfo('Salvando...');
		DemandaService.salvardemanda($ctrl.demanda, function(data){
			share.demanda = data;
			$ctrl.demanda = data;
			configuraritensfaturamento(data);
			configurarorcamento(data);
			$ctrl.listacentroresultadoshoras = DemandaService.buscarcentroresultadoshora(data.id, $ctrl.changeatividade);
			MessageService.messagesuccess('Salvo com sucesso!')
		});
	}
	
	$ctrl.deletar = function () {
		DemandaService.deletardemanda($ctrl.demanda.id, function(data){
			$window.location.href = '/demandas/';
		});
	}
	
});