"use strict";

var gestor = angular.module('gestor', ['gestor-services', 'commons', 'ui.bootstrap', 'ui.mask', 'ngMaterial', 'ngMessages']);

gestor.controller('GestorController', function (GestorService, CommonsService, $scope, $window, $uibModal, $mdDialog){
	var $ctrl = this;
	$ctrl.show=true;
	
	var configurarregistros = data => {
		for  (let cliente of data){
			for (let demanda of cliente.demandas){
				for (let fase_atividade of demanda.fase_atividades) {
					for (let atividade of fase_atividade.atividades) {
						for (let atividade_profissional of atividade.atividadeprofissionais){
							if (atividade_profissional.horas_alocadas_milisegundos){
								atividade_profissional.horas_alocadas = CommonsService.milliparahoras(atividade_profissional.horas_alocadas_milisegundos);
							}
							
							if (atividade_profissional.quantidade_horas && atividade_profissional.quantidade_horas.toString().indexOf(':00') < 0){
								atividade_profissional.quantidade_horas_formatada = atividade_profissional.quantidade_horas + ':00';							
							}
						}
					}
				}
			}
		}
	}
	
	$ctrl.demandamap = {} 
	
	$ctrl.expandir = demanda => {
		if (!$ctrl.demandamap[demanda.$$hashKey]){
			$ctrl.demandamap[demanda.$$hashKey] = {};
		}
		$ctrl.demandamap[demanda.$$hashKey].expandir = !$ctrl.demandamap[demanda.$$hashKey].expandir; 
	}
	
	$ctrl.clientes = GestorService.buscarclientesdemandas(configurarregistros);
	
});
