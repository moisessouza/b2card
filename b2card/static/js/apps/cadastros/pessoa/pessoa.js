"use strict";

var pessoa = angular.module('pessoa', ['pessoa-services', 'centrocusto-services', 'commons', 'ui.bootstrap', 'ui.mask']);

pessoa.controller('PessoaController', function ($scope, $window, PessoaService, CentroCustoService){
	var $ctrl = this;
	
	$ctrl.show = true;
	
	$ctrl.listacentrocusto = CentroCustoService.buscarcentrocustos();
	
	$ctrl.pessoa = {
		enderecos:[{}],
		telefones:[{}],
		dados_bancarios:[{}]
	}
	
	$ctrl.adicionarendereco = function () {
		$ctrl.pessoa.enderecos.push({});
	}
	
	$ctrl.adicionartelefone = function () {
		$ctrl.pessoa.telefones.push({});
	}
	
	$ctrl.adicionardadosbancarios = function () {
		$ctrl.pessoa.dados_bancarios.push({});
	}
	
	$ctrl.remover = function (objeto) {
		objeto.remover=true;
	}
	
}).controller('ListPessoaController', function ($scope, $window, PessoaService){
	var $ctrl = this;
});