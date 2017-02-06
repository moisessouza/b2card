"use strict";

var gestor = angular.module('gestor', ['gestor-services', 'commons', 'ui.bootstrap', 'ui.mask', 'ngMaterial', 'ngMessages']);

gestor.controller('GestorController', function (GestorService, CommonsService, $scope, $window, $uibModal, $mdDialog){
	var $ctrl = this;
	$ctrl.show=true;
	
	var configurarregistros = data => {
		for  (let cliente of data){
			for (let demanda of cliente.demandas){
				if (demanda.fase_atividades){
					for (let fase_atividade of demanda.fase_atividades) {
						if (fase_atividade.atividades){
							for (let atividade of fase_atividade.atividades) {
								for (let atividade_profissional of atividade.atividadeprofissionais){
									if (atividade_profissional.horas_alocadas_milisegundos){
										atividade_profissional.horas_alocadas = CommonsService.milliparahoras(atividade_profissional.horas_alocadas_milisegundos);
									}
									
									if (atividade_profissional.quantidade_horas && atividade_profissional.quantidade_horas.toString().indexOf(':00') < 0){
										atividade_profissional.quantidade_horas_formatada = atividade_profissional.quantidade_horas + ':00';
										
										if (atividade_profissional.horas_alocadas_milisegundos){
											var milisegundos = atividade_profissional.quantidade_horas * 60 * 60 * 1000;
											
											if (atividade_profissional.horas_alocadas_milisegundos > milisegundos){
												atividade_profissional.atrasado = true;
											}
										}
										
									}
								}
							}
						}
					}
				}
			}
		}
	}
	
	$ctrl.status = {
		'O': true,
		'D': true,
		'A': true,
		'H': true
	}
	
	$ctrl.demandamap = {} 
	
	$ctrl.abrirmodalstatus = () => {
		$ctrl.showmodal = !$ctrl.showmodal; 
	}
	
	$ctrl.expandir = demanda => {
		if (!$ctrl.demandamap[demanda.$$hashKey]){
			$ctrl.demandamap[demanda.$$hashKey] = {};
		}
		$ctrl.demandamap[demanda.$$hashKey].expandir = !$ctrl.demandamap[demanda.$$hashKey].expandir;
		
		if ($ctrl.demandamap[demanda.$$hashKey].expandir) {
			GestorService.buscaratividadesdemanda(demanda.id, function (data) {
				demanda.fase_atividades = data
				configurarregistros($ctrl.clientes);
			});
		}
	}
	
	$ctrl.redirecionar = id => {
		$window.location.href = BASE_URL + 'demandas/editar/' + id;
	}
	
	$ctrl.clientes = GestorService.buscarclientesdemandas($ctrl.status, configurarregistros);
	
	$ctrl.pesquisar = () => {
		$ctrl.clientes = GestorService.buscarclientesdemandas($ctrl.status, configurarregistros);
	}
	
});
