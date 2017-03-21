"use strict";

var inicial = angular.module('inicial', ['inicial-services', 'tipoalocacao-services', 'tipodespesa-services', 'commons', 'ui.bootstrap', 'ui.mask', 'ngMaterial', 'ngMessages']);

inicial.controller('InicialController', function (InicialService, CommonsService, $scope, $window, $uibModal, $mdDialog){
	var $ctrl = this;
	$ctrl.show=true;
	
	var configurarregistros = data => {
		for(let cliente of data) {
			for (let demanda of cliente.demandas) {
				if (demanda.fase_atividades){
					for (let fase_atividade of demanda.fase_atividades) {
						for (let atividade of fase_atividade.atividades) {
							if (atividade.atividade_profissional){
								if (atividade.atividade_profissional.horas_alocadas_milisegundos){
									atividade.atividade_profissional.horas_alocadas = CommonsService.milliparahoras(atividade.atividade_profissional.horas_alocadas_milisegundos);
								}
								
								if (atividade.atividade_profissional.quantidade_horas && atividade.atividade_profissional.quantidade_horas.toString().indexOf(':00') < 0){
									atividade.atividade_profissional.quantidade_horas = atividade.atividade_profissional.quantidade_horas + ':00';	
									
									if (atividade.atividade_profissional.horas_alocadas_milisegundos){
										var horas = parseInt(atividade.atividade_profissional.quantidade_horas.split(':')[0])
										var milisegundos = horas * 60 * 60 * 1000;
										
										if (atividade.atividade_profissional.horas_alocadas_milisegundos > milisegundos){
											atividade.atividade_profissional.atrasado = true;
										}
									}
									
								}
							}
						}
					}
				}
				demanda.id = CommonsService.pad(demanda.id, 4);
			}
		}
	}
	
	$ctrl.status = {
		'D': true,
		'H': true,
	}
	
	$ctrl.abrirmodalalocacao = (ev, atividade) => {
		
		var modalInstance = $uibModal.open({
			animation : $ctrl.animationsEnabled,
			ariaLabelledBy : 'modal-title',
			ariaDescribedBy : 'modal-body',
			templateUrl : '/static/modal/modalAlocacao.html?bust=' + Math.random().toString(36).slice(2),
			controller : 'ModalAlocacaoController',
			controllerAs : '$ctrl',
			//size : 'lg'
			windowClass: 'app-modal-window',
			resolve : {
		    	  atividade: atividade
			}
		});
			
		modalInstance.result.then(function(data) {
			InicialService.buscaratividadesprofissionalporatividade(atividade.id, function (data){
				atividade.atividade_profissional = data;
				configurarregistros($ctrl.clientes);
			});
		}, function() {
			// $log.info('Modal dismissed at: ' + new Date());
		});
		
	}
	
	$ctrl.demandamap = {} 
	
	$ctrl.expandir = demanda => {
		if (!$ctrl.demandamap[demanda.$$hashKey]){
			$ctrl.demandamap[demanda.$$hashKey] = {};
		}
		$ctrl.demandamap[demanda.$$hashKey].expandir = !$ctrl.demandamap[demanda.$$hashKey].expandir;
		if ($ctrl.demandamap[demanda.$$hashKey].expandir) {
			demanda.fase_atividades = InicialService.buscaratividadesprofissionalpordemandaid(demanda.id, function () {
				configurarregistros($ctrl.clientes);
			});
		}
	}
	
	$ctrl.expandirdemandainterna = demanda => {
		
		if (!$ctrl.demandamap[demanda.$$hashKey]){
			$ctrl.demandamap[demanda.$$hashKey] = {};
		}
		$ctrl.demandamap[demanda.$$hashKey].expandir = !$ctrl.demandamap[demanda.$$hashKey].expandir;
		
		if ($ctrl.demandamap[demanda.$$hashKey].expandir) {
			demanda.fase_atividades = InicialService.buscaratividadesdemandainterna(demanda.id, function () {
				configurarregistros($ctrl.clientesinternos);
			});
		}
		
	}
	
	$ctrl.abrirmodalstatus = () => {
		$ctrl.showmodal = !$ctrl.showmodal; 
	}
	
	$ctrl.clientes = InicialService.buscaratividadesprofissional($ctrl.status, configurarregistros);
	
	$ctrl.clientesinternos = InicialService.buscaratividadesinternas($ctrl.statusinterno, configurarregistros);
	
	$ctrl.pesquisar = () => {
		$ctrl.clientes = InicialService.buscaratividadesprofissional($ctrl.status, configurarregistros);
	}
	
	$ctrl.pesquisarinterno = () => {
		$ctrl.clientesinternos = InicialService.buscaratividadesinternas($ctrl.statusinterno, configurarregistros);
	}
	
	$ctrl.abrirmodalalocacaointerna = (ev, atividade) => {
		
		var modalInstance = $uibModal.open({
			animation : $ctrl.animationsEnabled,
			ariaLabelledBy : 'modal-title',
			ariaDescribedBy : 'modal-body',
			templateUrl : '/static/modal/modalAlocacaoInterna.html?bust=' + Math.random().toString(36).slice(2),
			controller : 'ModalAlocacaoInternaController',
			controllerAs : '$ctrl',
			//size : 'lg'
			windowClass: 'app-modal-window',
			resolve : {
		    	  atividade: atividade
			}
		});
			
		modalInstance.result.then(function(data) {
			InicialService.buscaratividadesprofissionalporatividade(atividade.id, function (data){
				atividade.atividade_profissional = data;
				configurarregistros($ctrl.clientesinternos);
			});
		}, function() {
			// $log.info('Modal dismissed at: ' + new Date());
		});
		
	}
	
	
	$ctrl.abrirmodaldespesas = demanda => {
		
		var modalInstance = $uibModal.open({
			animation : $ctrl.animationsEnabled,
			ariaLabelledBy : 'modal-title',
			ariaDescribedBy : 'modal-body',
			templateUrl : '/static/modal/modalDespesas.html?bust=' + Math.random().toString(36).slice(2),
			controller : 'ModalDespesaController',
			controllerAs : '$ctrl',
			size : 'lg',
			windowClass: 'app-modal-window',
			resolve : {
		    	  demanda: demanda
			}
		});
			
		modalInstance.result.then(function(data) {
		}, function() {
		});
	}
	
}).controller('ModalDespesaController', function (demanda, InicialService, TipoDespesaService, CommonsService, TipoAlocacaoService, $uibModalInstance, $scope, $window) {
	var $ctrl = this;
	
	$ctrl.selecionarlote = lote => {
		$ctrl.lote_despesa = lote;
	};
	
	$ctrl.lotes_abertos = InicialService.buscarlotesemaberto(demanda.id, data => {
		if (data.length <= 0) {
			$ctrl.lote_despesa = {
				demanda: demanda,
				item_despesas: []
			};
		}
	});
	
	$ctrl.tipo_despesas = TipoDespesaService.buscartipodespesas();
	
	$ctrl.adicionar = () => {
		$ctrl.lote_despesa.item_despesas.push({});
	};
	
	$ctrl.remover = (despesa) => {
		despesa.remover = true;
	};
	
	$ctrl.cancelar= function (){
		$uibModalInstance.close();
	};
	
	$ctrl.salvar = () => {
		$ctrl.lote_despesa = InicialService.salvarlotedespesa($ctrl.lote_despesa, function (data) {
			$uibModalInstance.close(data);
		});
	};
	
}).controller('ModalAlocacaoInternaController', function (atividade, InicialService, CommonsService, TipoAlocacaoService, $uibModalInstance, $scope, $window) {
	
	var $ctrl = this;
	$ctrl.atividade = atividade;
	
	$scope.today = function() {
		$ctrl.data =new Date();
	};
	$scope.today();

	$scope.clear = function() {
		$scope.dt = null;
	};

	$ctrl.abrir = function() {
		$ctrl.aberto = true;
	};
	
	$ctrl.cancelar= function (){
		$uibModalInstance.close();
	}
	
	$ctrl.salvar = () => {
		
		let data = CommonsService.dataparaurl($ctrl.data);
		
		InicialService.validardatahora (data, $ctrl.hora_inicio, $ctrl.hora_fim, function(result) {
			
			if(result.custo_prestador && !result.possui_alocacao) {
				
				if (!$ctrl.data) {
					alert('Informe data.')
					return;
				}
				
				if (!$ctrl.hora_inicio){
					alert('Informe hora inicio.');
					return;
				}
				
				if(!$ctrl.hora_fim) {
					alert('Informe hora fim.');
					return;
				}
				
				var hora_inicio = $ctrl.hora_inicio.split(':');
				var hora_fim = $ctrl.hora_fim.split(':');
				
				hora_inicio = new Date(0, 0, 0, hora_inicio[0], hora_inicio[1], 0, 0);
				hora_fim = new Date(0,0,0,hora_fim[0], hora_fim[1], 0,0).getTime();
				
				if (hora_inicio >= hora_fim) {
					alert('Hora inicio deve ser menor que hora fim.');
					return;
				}
				
				var milisegundos = hora_fim - hora_inicio
				
				if ($ctrl.data instanceof Date){
					$ctrl.data = CommonsService.dataparastring($ctrl.data);
				}
				
				if (atividade.atividade_profissional) {
					var data = {
						atividade_profissional: atividade.atividade_profissional,
						horas_alocadas_milisegundos : milisegundos,
						hora_inicio: $ctrl.hora_inicio,
						hora_fim: $ctrl.hora_fim,
						data_informada: $ctrl.data,
						observacao: $ctrl.observacao
					}
				} else {
					var data = {
						atividade: atividade,
						horas_alocadas_milisegundos : milisegundos,
						hora_inicio: $ctrl.hora_inicio,
						hora_fim: $ctrl.hora_fim,
						data_informada: $ctrl.data,
						observacao: $ctrl.observacao
					}	
				}
				
				InicialService.salvaralocacaointerna(data, function (){
					$uibModalInstance.close(data);
				});
				
			} else {
				if (result.possui_alocacao){
					alert('Você já possui alocação no horário especificado');
				} else {
					alert('Você não possui cadastro de custo prestador ou vigência para esta data, favor verificar!');	
				}
			}
			
		});
		
	}
	
}).controller('ModalAlocacaoController', function (atividade, InicialService, CommonsService, TipoAlocacaoService, $uibModalInstance, $scope, $window) {
	var $ctrl = this;
	$ctrl.atividade = atividade;
	$ctrl.atividade_fechada;
	
	InicialService.buscarultimaalocacao(atividade.atividade_profissional.id, function (data){
		$ctrl.percentual_conclusao = data.percentual_concluido;
		if (data.percentual_concluido == 100){
			$ctrl.atividade_fechada = true;
		}
	});
	
	$ctrl.tipoalocacaolist = TipoAlocacaoService.buscartipoalocacoes();
	
	$scope.today = function() {
		$ctrl.data =new Date();
	};
	$scope.today();

	$scope.clear = function() {
		$scope.dt = null;
	};

	$ctrl.abrir = function() {
		$ctrl.aberto = true;
	};
	
	$ctrl.cancelar= function (){
		$uibModalInstance.close();
	}
	
	$ctrl.validarpercentualconclusao = function () {
		if ($ctrl.percentual_conclusao > 100) {
			$ctrl.percentual_conclusao = 100;
		}
	}
	
	$ctrl.salvar = () => {
		
		let data = CommonsService.dataparaurl($ctrl.data);
		
		InicialService.validardatahora (data, $ctrl.hora_inicio, $ctrl.hora_fim, function(result) {
			
			if(result.custo_prestador && !result.possui_alocacao) {
				
				if (!$ctrl.data) {
					alert('Informe data.')
					return;
				}
				
				if (!$ctrl.percentual_conclusao) {
					alert('Informe % conclusão.');
					return;
				}
				
				if (!$ctrl.hora_inicio){
					alert('Informe hora inicio.');
					return;
				}
				
				if(!$ctrl.hora_fim) {
					alert('Informe hora fim.');
					return;
				}
				
				if($ctrl.atividade_fechada && (!$ctrl.tipo_alocacao || !$ctrl.tipo_alocacao.id)) {
					alert('Informe tipo de alocação.');
					return;
				}
				
				var hora_inicio = $ctrl.hora_inicio.split(':');
				var hora_fim = $ctrl.hora_fim.split(':');
				
				hora_inicio = new Date(0, 0, 0, hora_inicio[0], hora_inicio[1], 0, 0);
				hora_fim = new Date(0,0,0,hora_fim[0], hora_fim[1], 0,0).getTime();
				
				if (hora_inicio >= hora_fim) {
					alert('Hora inicio deve ser menor que hora fim.');
					return;
				}
				
				var milisegundos = hora_fim - hora_inicio

				if ($ctrl.data instanceof Date){
					$ctrl.data = CommonsService.dataparastring($ctrl.data);
				}
				
				var data = {
					atividade_profissional: atividade.atividade_profissional,
					horas_alocadas_milisegundos : milisegundos,
					percentual_concluido : $ctrl.percentual_conclusao,
					hora_inicio: $ctrl.hora_inicio,
					hora_fim: $ctrl.hora_fim,
					data_informada: $ctrl.data,
					observacao: $ctrl.observacao,
					tipo_alocacao: $ctrl.tipo_alocacao
				}

				InicialService.salvaralocacao(data, function (){
					$uibModalInstance.close(data);
				});
				
			} else {
				if (result.possui_alocacao){
					alert('Você já possui alocação no horário especificado');
				} else {
					alert('Você não possui cadastro de custo prestador ou vigência para esta data, favor verificar!');	
				}
			}
		});
		
	}
	
});
