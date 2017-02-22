"use strict";

var contasreceber = angular.module('contasreceber', ['contasreceber-service', 'parcela-services', 'pessoa-services', 'demandas-services', 'pesquisademanda-services', 'valorhora-services', 'parcela', 'commons', 'ui.bootstrap', 'ui.mask']);

contasreceber.controller('ContasReceberController', function ($scope, $window, $uibModal, DemandaService, PessoaService, PesquisaDemandaService,ContasReceberService, ValorHoraService, ParcelaService, CommonsService){
	var $ctrl = this;
	
	$ctrl.show = true;
	
	var date = new Date();
	
	var mes = (date.getMonth() + 1) + "/" + date.getFullYear();
	
	$ctrl.listaclientes= PessoaService.buscarpessoasjuridicas();
	
	$ctrl.arguments = {
		'mes': mes,
		'ordenar':false,
		'pagina': 1,
	}
	
	$ctrl.pesquisar = function () {
		PesquisaDemandaService.buscardemandas($ctrl.arguments, function (data) {
			$ctrl.resultados = data.demandas;
		});
	}
	
	$ctrl.listaitensfaturamento = [];
	
	var verificarsejaselecionado = lista_selecionada => {
		if ($ctrl.listaitensfaturamento) {
			
		} 
	}
	
	$ctrl.abrirparcelas = function (demanda) {
		
		ParcelaService.buscarorcamentopordemandaid(demanda.id, function(data){
			demanda.orcamento = data;
			$ctrl.listafases = data.fases;
			
			for (let fase of data.fases) {
				for (let itemfase of fase.itensfase) {
					itemfase.valor_total = CommonsService.formatarnumero(itemfase.valor_total);
				}
			}
			
			ValorHoraService.buscarvalorhoraporcliente(demanda.cliente.id, function (data) {
				
				var listavalorhora = data;
				$ctrl.listavalorhora = data;
				
				demanda.orcamento.total_orcamento = CommonsService.formatarnumero(demanda.orcamento.total_orcamento);
				
				var modalInstance = $uibModal.open({
					animation : $ctrl.animationsEnabled,
					ariaLabelledBy : 'modal-title',
					ariaDescribedBy : 'modal-body',
					templateUrl : '/static/modal/modalItensFaturamento.html?bust=' + Math.random().toString(36).slice(2),
					controller : 'ModalParcelasController',
					controllerAs : '$ctrl',
					//size : 'lg'
					windowClass: 'app-modal-window',
					resolve : {
						demanda : function() {
							return demanda;
						},
						listavalorhora: function () {
							return listavalorhora;
						},
						lote_faturamento: true
					}
				});
					
				modalInstance.result.then(function(data) {
					$ctrl.listaitensfaturamento = $ctrl.listaitensfaturamento.concat(data);
				}, function() {
				});
				
			});
			
		});
		
	}
	
});
