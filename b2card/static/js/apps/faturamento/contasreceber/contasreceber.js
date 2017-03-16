"use strict";

var contasreceber = angular.module('contasreceber', ['contasreceber-service', 'parcela-services', 'pessoa-services', 'demandas-services', 'fase-services', 'pesquisademanda-services', 'valorhora-services', 'parcela', 'commons', 'ui.bootstrap', 'ui.mask']);

contasreceber.controller('ContasReceberController', function ($scope, $window, $uibModal, DemandaService, PessoaService, PesquisaDemandaService,ContasReceberService, ValorHoraService, ParcelaService, FaseService, CommonsService){
	var $ctrl = this;
	
	$ctrl.show = true;
	
	var date = new Date();
	
	var mes = (date.getMonth() + 1) + "/" + date.getFullYear();
	
	$ctrl.listaclientes= PessoaService.buscarclientes();
	
	$ctrl.arguments = {
		'mes': mes,
		'ordenar':false,
		'pagina': 1,
	}
	
	FaseService.buscarfases(function (data) {
		 $ctrl.listafases = data;	
	});
	
	$ctrl.listavalorhora = ValorHoraService.buscarvalorhoras();
	
	$ctrl.pesquisar = function () {
		PesquisaDemandaService.buscardemandaunidadeadministrativa($ctrl.arguments, function (data) {
			$ctrl.resultados = data.demandas;
		});
	}
	
	$ctrl.buscarpacotecliente = () => {
		$ctrl.resultados = [];
		ContasReceberService.buscarpacoteitensclienteid($ctrl.arguments.cliente_id, function (data){
			$ctrl.pacote_itens = data;
			$ctrl.listaitensfaturamento = data.lista_itens;
			$ctrl.calculartotal(data.lista_itens);
		});
	};
	
	$ctrl.listaitensfaturamento = [];
	
	$ctrl.calculartotal = (data) => {
		
		$ctrl.totalhoras = 0;
		$ctrl.totalvalor = 0;
		
		if (data) {
			for (let itemfaturamento of data) {
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
		$ctrl.totalhoras = CommonsService.arredondar($ctrl.totalhoras);
	}
	
	$ctrl.abrirparcelas = function (demanda) {
		
		ParcelaService.buscarorcamentopordemandaid(demanda.id, function(data){
			demanda.orcamento = data;
			
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
						
						if (!$ctrl.listaitensfaturamento){
							$ctrl.listaitensfaturamento = [];
						}
						
						for (let item of data){
							if (item.pacote_itens == null || !item.pacote_itens && !item.pacote_itens.id) {
								$ctrl.listaitensfaturamento.push(item);
							}
						}
						
						$ctrl.calculartotal($ctrl.listaitensfaturamento);
						
						let listaitens = $ctrl.listaitensfaturamento;
						$ctrl.listaitensfaturamento = [];
						
						let context = {
							'id': $ctrl.pacote_itens ? $ctrl.pacote_itens.id : null,
							'cliente_id': $ctrl.arguments.cliente_id,		
							'valor_total': $ctrl.totalvalor,
							'total_horas': $ctrl.totalhoras,
							'lista_itens': listaitens
						}
						
						$ctrl.pacote_itens = ContasReceberService.gerarpacoteitens(context, function () {
							ContasReceberService.buscarpacoteitensclienteid($ctrl.arguments.cliente_id, function (result){
								$ctrl.pacote_itens = result;
								$ctrl.listaitensfaturamento = result.lista_itens;
								$ctrl.calculartotal(result.lista_itens);
							});
						});
					}
				}, function() {
				});
				
			});
			
		});
	}
	
	$ctrl.remover = parcela =>{
		if ($ctrl.listaitensfaturamento) {
			$ctrl.listaitensfaturamento.splice($ctrl.listaitensfaturamento.indexOf(parcela), 1);
			$ctrl.calculartotal($ctrl.listaitensfaturamento);
			
			let context = {
				'id': $ctrl.pacote_itens ? $ctrl.pacote_itens.id : null,
				'cliente_id': $ctrl.arguments.cliente_id,	
				'valor_total': $ctrl.totalvalor,
				'total_horas': $ctrl.totalhoras,
				'lista_itens': $ctrl.listaitensfaturamento
			}
				
			$ctrl.pacote_itens = ContasReceberService.gerarpacoteitens(context, function () {
				ContasReceberService.buscarpacoteitensclienteid($ctrl.arguments.cliente_id, function (data){
					$ctrl.pacote_itens = data;
					$ctrl.listaitensfaturamento = data.lista_itens;
					$ctrl.calculartotal(data.lista_itens);
				});
			});
		}
	}
	
	$ctrl.abrirarquivoaprovacao = pacote_itens_id => {
		$window.open(BASE_URL + 'faturamento/gerar_arquivo_aprovacao/' + pacote_itens_id, '_blank');
	}
	
	$ctrl.enviarparaaprovacao = () => {
		
		var data = {
			'id': $ctrl.pacote_itens ? $ctrl.pacote_itens.id : null,
		}
		
		ContasReceberService.enviarparaaprovacao(data, function () {
			ContasReceberService.buscarpacoteitensclienteid($ctrl.arguments.cliente_id, function (data){
				$ctrl.abrirarquivoaprovacao(data.id);
				$ctrl.pacote_itens = data;
				$ctrl.listaitensfaturamento = data.lista_itens;
				$ctrl.calculartotal(data.lista_itens);
			});
		});
	}
	
	$ctrl.enviarparafaturamento = () => {
		var data = {
			'id': $ctrl.pacote_itens ? $ctrl.pacote_itens.id : null,
		}
		
		ContasReceberService.enviarparafaturamento(data, function () {
			ContasReceberService.buscarpacoteitensclienteid($ctrl.arguments.cliente_id, function (data){
				$ctrl.pacote_itens = data;
				$ctrl.listaitensfaturamento = data.lista_itens;
				$ctrl.calculartotal(data.lista_itens);
			});
		});
	}
	
});
