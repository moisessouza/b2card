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
			configurardemanda(share.demanda.id);
		}, function() {
			// $log.info('Modal dismissed at: ' + new Date());
		});
		
	}
	
	$ctrl.clientes = InicialService.buscaratividadesprofissional();
	
}).controller('ModalAlocacaoController', function (atividade, CommonsService, $scope, $window) {
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
	
	$ctrl.salvar = () => {
		
		var hora_inicio = $ctrl.hora_inicio.split(':');
		var hora_fim = $ctrl.hora_fim.split(':');
		
		hora_inicio = moment(new Date(0, 0, 0, hora_inicio[0], hora_inicio[1], 0, 0).getTime());
		console.log(hora_inicio);
		
		hora_fim = moment(new Date(0,0,0,hora_fim[0], hora_fim[1], 0,0).getTime());
		console.log(hora_fim);
		
		var data = new Date();
		data.setTime(hora_fim - hora_inicio)
		
		console.log(CommonsService.milliparahoras(hora_fim - hora_inicio))
		
	}
	
});
