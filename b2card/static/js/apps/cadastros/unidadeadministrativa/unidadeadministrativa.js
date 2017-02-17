"use strict";

var centrocusto = angular.module('unidadeadministrativa', ['unidadeadministrativa-services', 'commons', 'ui.bootstrap', 'ui.mask']);

centrocusto.controller('UnidadeAdministrativaController', function ($scope, $window, CommonsService, UnidadeAdministrativaService){
	var $ctrl = this;
	
	$ctrl.unidadeadministrativa = {}
	
	$ctrl.show =true;
	
	var formatar_dados = function(data) {
		if (data) {
			for (let i of data) {
				i.custo_operacao_hora = CommonsService.formatarnumero(i.custo_operacao_hora);
			}
		}
	};
	
	$ctrl.unidadeadministrativalist = UnidadeAdministrativaService.buscarunidadeadministrativas(formatar_dados);
	
	$ctrl.salvar = function () {
		UnidadeAdministrativaService.salvar($ctrl.unidadeadministrativa, function () {
			$ctrl.unidadeadministrativalist = UnidadeAdministrativaService.buscarunidadeadministrativas(formatar_dados);
			$ctrl.unidadeadministrativa = {};
		});
	}
	
	$ctrl.deletar = function (data) {
		if(confirm(MESSAGE_EXCLUIR)) {
			UnidadeAdministrativaService.deletar(data, function () {
				$ctrl.unidadeadministrativalist = UnidadeAdministrativaService.buscarunidadeadministrativas();
			});
		}
	}
	
	$ctrl.editar = function (data) {
		$ctrl.unidadeadministrativa = data;
	}
	
	$ctrl.novo = function () {
		$ctrl.unidadeadministrativa = {};
	}
	
});