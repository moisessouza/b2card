"use strict";

var valorhora = angular.module('valorhora', ['valorhora-services', 'centrocusto-services', 'centroresultado-services', 
                                             'contagerencial-services',	'naturezaoperacao-services', 'tipohora-services',
                                             'commons', 'ui.bootstrap', 'ui.mask']);

valorhora.controller('ValorHoraController', function (ValorHoraService, CentroCustoService, 
		CentroResultadoService, ContaGerencialService, NaturezaOperacaoService, TipoHoraService, CommonsService){
	var $ctrl = this;
	
	var messageinfo = function (msg){
		$ctrl.clazz = 'label-primary';	
		$ctrl.message = msg;
	}

	var messagesuccess = function (msg) {
		$ctrl.clazz = 'label-success';
		$ctrl.message = msg;
	}
	
	if (valor_hora_id){
		ValorHoraService.buscarvalorhora(valor_hora_id, function(data){
			$ctrl.valorhora = data;
			
			if (data.vigencias){
				for(var i in data.vigencias){
					var vigencia = data.vigencias[i];
					vigencia.valor = CommonsService.formatarnumero(vigencia.valor);
				}
			} else {
				data.vigencias = [];
			}
			
			$ctrl.show=true;
		});
	} else {
		$ctrl.valorhora = {
			'vigencias': []
		}	
		$ctrl.show=true;
	}
	
	$ctrl.centrocustolist = CentroCustoService.buscarcentrocustos();
	$ctrl.centroresultadolist = CentroResultadoService.buscarcentroresultados();
	$ctrl.contagerenciallist = ContaGerencialService.buscarcontagerenciais();
	$ctrl.naturezaoperacaolist = NaturezaOperacaoService.buscarnaturezaoperacoes();
	$ctrl.tipohoralist = TipoHoraService.buscartipohoras();
	
	$ctrl.salvar = function (){
		messageinfo("salvando...");
		ValorHoraService.salvar($ctrl.valorhora, function (data){
			$ctrl.valorhora = data;
			
			if (data.vigencias){
				for(var i in data.vigencias){
					var vigencia = data.vigencias[i];
					vigencia.valor = CommonsService.formatarnumero(vigencia.valor);
				}
			} else {
				data.vigencias = [];
			}
			
			messagesuccess('salvo!')
		});
	}
	
	$ctrl.adicionarvigencia = function (){
		$ctrl.valorhora.vigencias.push({})
	}
	
	$ctrl.deletar = function () {
		if(confirm(MESSAGE_EXCLUIR)) {
			ValorHoraService.deletar($ctrl.valorhora.id, function(data) {
				window.location.replace(BASE_URL + 'cadastros/valorhora/');	
			});
		}
	}
	
});