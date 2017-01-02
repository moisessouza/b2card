"use strict";

var pessoa = angular.module('pessoa', ['pessoa-services', 'centrocusto-services', 'commons', 'ui.bootstrap', 'ui.mask']);

pessoa.controller('PessoaController', function ($scope, $window, PessoaService, CentroCustoService, MessageService){
	var $ctrl = this;
	
	$ctrl.show = true;
	
	if (pessoa_id) {
		$ctrl.pessoa = PessoaService.buscarpessoa(pessoa_id)
	} else {
		$ctrl.pessoa = {
			enderecos:[{}],
			telefones:[{}],
			dados_bancarios:[{}]
		}
	}
	
	$ctrl.listacentrocusto = CentroCustoService.buscarcentrocustos();
	
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
	
	$ctrl.salvar = function () {
		$ctrl.pessoa = PessoaService.salvarpessoa($ctrl.pessoa, function () {
			MessageService.messagesuccess('Cadastro realizado com sucesso!');
		});
	}
	
	$ctrl.deletarpessoa = function (){
		PessoaService.deletarpessoa($ctrl.pessoa.id, function () {
			$window.location.href = '/cadastros/pessoa/';
		});
	}
	
	$ctrl.changenumeroconta = function (dado_bancario){
		dado_bancario.cod_agencia = dado_bancario.cod_agencia.replace(/[^0-9\-]/g, '');
	}
	
}).controller('ListPessoaController', function ($scope, $window, PessoaService){
	var $ctrl = this;
	
	$ctrl.pessoas = PessoaService.buscarpessoas();
	
	$ctrl.redirecionar = function (pessoa) {
		$window.location.href = '/cadastros/pessoa/editar/' + pessoa.id
	}
	
});