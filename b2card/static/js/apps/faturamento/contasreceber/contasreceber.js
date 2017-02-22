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
	
	var verificarsejaselecionado = selecionado => {
		if ($ctrl.listaitensfaturamento && selecionado) {
			for (let itensfaturamento of $ctrl.listaitensfaturamento) {
				if (selecionado.id == itensfaturamento.id) {
					return true;
				}
			}
		}
		return false;
	}
	
	$ctrl.calculartotal = () => {
		
		$ctrl.totalhoras = 0;
		$ctrl.totalvalor = 0;
		
		if ($ctrl.listaitensfaturamento) {
			for (let itemfaturamento of $ctrl.listaitensfaturamento) {
				if (itemfaturamento.parcelafases) {
					for (let parcelafase of itemfaturamento.parcelafases){
						if (parcelafase.medicoes){
							for(let medicao of parcelafase.medicoes){
								$ctrl.totalhoras+=medicao.quantidade_horas;
							}
						}
					}
				}
				$ctrl.totalvalor+=CommonsService.stringparafloat(itemfaturamento.valor_parcela);
			}
		}
		
		$ctrl.totalvalor = CommonsService.formatarnumero($ctrl.totalvalor);
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
						lote_faturamento: function () {
							return true;
						},
						listaitensfaturamento: function () {
							return $ctrl.listaitensfaturamento;
						}
					}
				});
					
				modalInstance.result.then(function(data) {
					if (data) {
						for (let selecionado of data) {
							if (!verificarsejaselecionado(selecionado)) {
								$ctrl.listaitensfaturamento.push(selecionado);
							}
						}
						$ctrl.calculartotal();
					}
				}, function() {
				});
				
			});
			
		});
	}
	
	$ctrl.remover = parcela =>{
		if ($ctrl.listaitensfaturamento) {
			$ctrl.listaitensfaturamento.splice($ctrl.listaitensfaturamento.indexOf(parcela), 1);
			$ctrl.calculartotal();
		}
	}
	
	$ctrl.enviarparaaprovacao = () => {
		
		var data = {
			'id': $ctrl.lote_faturamento_id,
			'valor_total': $ctrl.valor_total,
			'total_horas': $ctrl.total_horas,
			'lista_itens': $ctrl.listaitensfaturamento
		}
		
		ContasReceberService.gerarlotefaturamento(data, function (data) {
			$ctrl.lote_faturamento_id = data.id;
		});
	}
	
	$ctrl.enviarparafaturamento = () => {
		alert('enviar para faturamento');
	}
	
});
