"use strict";

var relatorio_lancamentos = angular.module('relatorio_lancamentos', ['relatorio_lancamentos-services', 'pessoa-services', 'demandas-services', 'commons', 'ui.bootstrap', 'ui.mask', 'ngMaterial']);

relatorio_lancamentos.controller('RelatorioLancamentosController', function (RelatorioLancamentosService, PessoaService, DemandaService, CommonsService, $scope, $window){
	var $ctrl = this;
	
	$ctrl.modaldata = {}
	
	$ctrl.listaclientes= PessoaService.buscarpessoasjuridicas();
	$ctrl.listafuncionarios = PessoaService.buscarprofissionais();
	
	$ctrl.datepicker_options = {
		datepickerMode: 'month',
		minMode: 'month'
	}

	$ctrl.listademandas = [];
	
	$ctrl.abrirmodaldata = prop => {
		$ctrl.modaldata[prop] = !$ctrl.modaldata[prop] 
	}
	
	$ctrl.buscardemandas = (texto) => {
		DemandaService.buscardemandaportexto(texto, function (data) {
			
			for(let demanda of data) {
				demanda.nome_demanda = CommonsService.pad(demanda.id, 5) + ' - ' + demanda.nome_demanda;
			}
			
			$ctrl.listademandas = data;
		});	
	}
	
	$ctrl.listaalocacao = [];
	
	$ctrl.pesquisar = () => {
		$ctrl.listaalocacao = RelatorioLancamentosService.pesquisar($ctrl.arguments, function (data){
			for(let alocacao of data) {
				alocacao.horas_alocadas = CommonsService.milliparahoras(alocacao.horas_alocadas_milisegundos);
			}
		});
	}
	
});