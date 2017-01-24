"use strict";

var inicial = angular.module('inicial', ['inicial-services', 'commons', 'ui.bootstrap', 'ui.mask', 'ngMaterial', 'ngMessages']);

inicial.controller('InicialController', function (InicialService, $scope, $window, $uibModal, $mdDialog){
	var $ctrl = this;
	$ctrl.show=true;
	
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
			$ctrl.clientes = InicialService.buscaratividadesprofissional();
		}, function() {
			// $log.info('Modal dismissed at: ' + new Date());
		});
		
	}
	
	$ctrl.clientes = InicialService.buscaratividadesprofissional();
	
}).controller('ModalAlocacaoController', function (atividade, InicialService, CommonsService, $uibModalInstance, $scope, $window) {
	var $ctrl = this;
	$ctrl.atividade = atividade;
	
	$scope.today = function() {
		$scope.dt = new Date();
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
		
		var hora_inicio = $ctrl.hora_inicio.split(':');
		var hora_fim = $ctrl.hora_fim.split(':');
		
		hora_inicio = new Date(0, 0, 0, hora_inicio[0], hora_inicio[1], 0, 0);
		hora_fim = new Date(0,0,0,hora_fim[0], hora_fim[1], 0,0).getTime();
		
		var milisegundos = hora_fim - hora_inicio

		var data = {
			atividade_profissional: atividade.atividade_profissional,
			horas_alocadas_milisegundos : milisegundos,
			percentual_concluido : $ctrl.percentual_conclusao,
		}

		InicialService.salvaralocacao(data, function (){
			$uibModalInstance.close();
		});
		
	}
	
});
