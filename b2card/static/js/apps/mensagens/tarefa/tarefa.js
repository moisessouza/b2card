"use strict";

var tarefa = angular.module('tarefa', ['tarefa-services', 'pessoa-services', 'relatorio_lancamentos-services', 'commons', 'ui.bootstrap', 'ui.mask']);

tarefa.controller('TarefaController', function ($scope, $window, TarefaService, PessoaService, RelatorioLancamentosService, CommonsService){
	var $ctrl = this;
	
	$ctrl.tarefa = {}
	
	RelatorioLancamentosService.ehgestor(function (data){
		$ctrl.eh_gestor = data.gestor;
	});
	
	var ajustardados = data => {
		for(let tarefa of data){
			tarefa.data_texto = tarefa.data_criacao; 
			tarefa.data_criacao = CommonsService.stringparadata(tarefa.data_criacao);
		}
	}
	
	$ctrl.listafuncionarios = PessoaService.buscarprofissionais();
	
	$ctrl.show =true;
	
	$ctrl.tarefalist = TarefaService.buscartarefas(function (data){
		ajustardados(data);
	});
	
	$ctrl.salvar = function () {
		TarefaService.salvar($ctrl.mensagem, function () {
			$ctrl.tarefalist = TarefaService.buscartarefas(function (data){
				ajustardados(data);
			});
			$ctrl.tarefa = {};
		});
	}
	
	$ctrl.deletar = function (data) {
		if(confirm(MESSAGE_EXCLUIR)) {
			TarefaService.deletar(data, function () {
				$ctrl.tarefalist = TarefaService.buscartarefas(function (data){
					ajustardados(data);
				});
			});
		}
	}
	
	$ctrl.editar = function (data) {
		$ctrl.mensagem = data;
	}
	
	$ctrl.novo = function () {
		$ctrl.mensagem = {};
	}
	
	$ctrl.abrirmodaldata = () => {
		$ctrl.modaldata = true;
	}
	
});