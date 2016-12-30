"use strict";

var pessoa = angular.module('pessoa', ['pessoa-services', 'centrocusto-services', 'commons', 'ui.bootstrap', 'ui.mask']);

pessoa.controller('PessoaController', function ($scope, $window, PessoaService, CentroCustoService){
	var $ctrl = this;
	
	$ctrl.listacentrocusto = CentroCustoService.buscarcentrocustos();
	
	$ctrl.pessoa = {
		enderecos:[{}],
		telefones:[{}],
		dados_bancarios:[{}]
	}
	
}).controller('ListPessoaController', function ($scope, $window, PessoaService){
	var $ctrl = this;
});