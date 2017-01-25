"use strict";

var inicial = angular.module('inicial', ['inicial-services', 'tipoalocacao-services', 'commons', 'ui.bootstrap', 'ui.mask', 'ngMaterial', 'ngMessages']);

inicial.controller('InicialController', function (InicialService, CommonsService, $scope, $window, $uibModal, $mdDialog){
	var $ctrl = this;
	$ctrl.show=true;
	
	var configurarregistros = data => {
		for(let cliente of data) {
			for (let demanda of cliente.demandas) {
				for (let fase_atividade of demanda.fase_atividades) {
					for (let atividade of fase_atividade.atividades) {
						if (atividade.atividade_profissional.horas_alocadas_milisegundos){
							atividade.atividade_profissional.horas_alocadas = CommonsService.milliparahoras(atividade.atividade_profissional.horas_alocadas_milisegundos);
						}
						
						if (atividade.atividade_profissional.quantidade_horas && atividade.atividade_profissional.quantidade_horas.toString().indexOf(':00') < 0){
							atividade.atividade_profissional.quantidade_horas = atividade.atividade_profissional.quantidade_horas + ':00';							
						}
					}
				}
				demanda.id = CommonsService.pad(demanda.id, 4);
			}
		}
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
	}
	
	$ctrl.clientes = InicialService.buscaratividadesprofissional(configurarregistros);
	
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
	
	$ctrl.salvar = () => {
		
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
			data_informada: $ctrl.data,
			observacao: $ctrl.observacao,
			tipo_alocacao: $ctrl.tipo_alocacao
		}

		InicialService.salvaralocacao(data, function (){
			$uibModalInstance.close(data);
		});
		
	}
	
});
