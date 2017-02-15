"use strict";

var pesquisademanda = angular.module('pesquisademanda', ['pesquisademanda-services', 'pessoa-services', 'ui.bootstrap', 'commons', 'ui.mask', 'ngMaterial']);

pesquisademanda.controller('PesquisaDemandaController', function (CommonsService, MessageService, PesquisaDemandaService, PessoaService, $window){
	var $ctrl = this;
	$ctrl.show=true;
	
	var configurarresultado = function (resultado) {
		if (resultado.demandas) {
			for(let demanda of resultado.demandas) {
				demanda.descricao = CommonsService.pad(demanda.id, 5) + ' - ' + demanda.cliente.nome_fantasia + ' - ' + demanda.nome_demanda;
			}
		}
	}
	
	$ctrl.listaclientes = PessoaService.buscarpessoasjuridicas();
	
	$ctrl.arguments = {
		pagina: '1',
		ordenar: false
	}
	
	$ctrl.resultado = PesquisaDemandaService.buscarcentroresultadoshora($ctrl.arguments, configurarresultado);
	
	$ctrl.abrirmodalstatus = () => {
		$ctrl.showmodal = !$ctrl.showmodal; 
	}
	
	$ctrl.ordenar = () => {
		$ctrl.arguments.ordenar = !$ctrl.arguments.ordenar
		$ctrl.pesquisar();
	}
	
	$ctrl.pesquisar = () => {
		$ctrl.arguments.status = $ctrl.status;
		$ctrl.resultado = PesquisaDemandaService.buscarcentroresultadoshora($ctrl.arguments, configurarresultado);
	}
	
	$ctrl.abrirdemanda = demanda => {
		$window.location.href = BASE_URL + 'demandas/editar/' + demanda.id
	}
	
	$ctrl.novo = () => {
		$window.location.href = BASE_URL + 'demandas/novo/'
	}
	
	$ctrl.abrirdatainicio = () => {
		$ctrl.data_inicio = true;
	}
	
	$ctrl.abrirdatafim = () => {
		$ctrl.data_fim = true;
	}
	
});