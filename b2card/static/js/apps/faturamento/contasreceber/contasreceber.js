"use strict";

var contasreceber = angular.module('contasreceber', ['contasreceber-service', 'parcela-services', 'demandas-services', 'valorhora-services', 'parcela', 'commons', 'ui.bootstrap', 'ui.mask']);

contasreceber.controller('ContasReceberController', function ($scope, $window, $uibModal, DemandaService, ContasReceberService, ValorHoraService, ParcelaService, CommonsService){
	var $ctrl = this;
	
	$ctrl.show = true;
	
	var date = new Date();
	
	var mes = (date.getMonth() + 1) + "/" + date.getFullYear();
	
	$ctrl.listaclientes= DemandaService.buscarclientes();
	
	$ctrl.arguments = {
			'mes': mes
	}
	
	$ctrl.pesquisar = function () {
		ContasReceberService.pesquisarcontasreceber($ctrl.arguments,function (data) {
			$ctrl.resultados = data;
			
			if (data.length <= 0) {
				$ctrl.messagem = 'Nenhum registro foi encontrado!';
			} else {
				$ctrl.messagem = null;
				for (let parcela of data) {
					parcela.valor_parcela = CommonsService.formatarnumero(parcela.valor_parcela);
					if (parcela.parcelafases){
						for (let parcelafase of parcela.parcelafases) {
							parcelafase.valor = CommonsService.formatarnumero(parcelafase.valor);
						}
					}
				}
			}
			
		});	
	}
	
	$ctrl.abrircontasreceber = function (contareceber) {
		
		ParcelaService.buscarorcamentopordemandaid(contareceber.demanda.id, function(data){
			contareceber.demanda.orcamento = data;
			
			for (let fase of data.fases) {
				for (let itemfase of fase.itensfase) {
					itemfase.valor_total = CommonsService.formatarnumero(itemfase.valor_total);
				}
			}
			
			ValorHoraService.buscarvalorhoraporcliente(contareceber.demanda.cliente.id, function (data) {
				
				var listavalorhora = data;
				
				contareceber.demanda.orcamento.total_orcamento = CommonsService.formatarnumero(contareceber.demanda.orcamento.total_orcamento);
				
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
							return contareceber.demanda;
						},
						listavalorhora: function () {
							return listavalorhora;
						}
						
					}
				});
					
				modalInstance.result.then(function(data) {
					$ctrl.pesquisar();
				}, function() {
					$ctrl.pesquisar();
				});
				
			});
			
		});
		
	}
	
});
