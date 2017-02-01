"use strict";

var pesquisademanda = angular.module('pesquisademanda', ['pesquisademanda-services', 'pessoa-services', 'ui.bootstrap', 'commons', 'ui.mask', 'ngMaterial']);

pesquisademanda.controller('PesquisaDemandaController', function (CommonsService, MessageService, PesquisaDemandaService, PessoaService, $window){
	var $ctrl = this;
	
	$ctrl.demandas = PesquisaDemandaService.buscarcentroresultadoshora();
	$ctrl.listaclientes = PessoaService.buscarpessoasjuridicas();
	
	$ctrl.pesquisar = () => {
		$ctrl.demandas = PesquisaDemandaService.buscarcentroresultadoshora($ctrl.arguments);
	}
	
	$ctrl.abrirdemanda = demanda => {
		$window.location.href = BASE_URL + 'demandas/editar/' + demanda.id
	}
	
	$ctrl.novo = () => {
		$window.location.href = BASE_URL + 'demandas/novo/'
	}
	
});