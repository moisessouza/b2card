"use strict";

var mensagens = angular.module('mensagens', ['mensagens-services', 'pessoa-services', 'commons', 'ui.bootstrap', 'ui.mask']);

mensagens.controller('MensagensController', function ($scope, $window, MensagensService, PessoaService){
	var $ctrl = this;
	$ctrl.show = true;
	
	$ctrl.listafuncionarios = PessoaService.buscarprofissionais();
	$ctrl.responsaveis = MensagensService.buscarresponsaveis();

	$ctrl.adicionar = () => {
		if (!$ctrl.responsaveis) {
			$ctrl.responsaveis = [];
		}
		$ctrl.responsaveis.push({});
	};
	
	$ctrl.salvar = () => {
		MensagensService.salvarresponsaveis($ctrl.responsaveis, function (data) {
			$ctrl.responsaveis = MensagensService.buscarresponsaveis();
		});
	};
	
	$ctrl.remover = responsavel_id =>{
		MensagensService.remover(responsavel_id, function (data) {
			$ctrl.responsaveis = MensagensService.buscarresponsaveis();
		});
	};
});