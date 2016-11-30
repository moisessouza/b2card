"use strict";

var faturamento = angular.module('faturamento', ['commons', 'ui.bootstrap', 'ui.mask']);

faturamento.controller('FaturamentoController', function ($scope, $window){
	var $ctrl = this;
	
	$ctrl.novo = function () {
		$ctrl.parcela = {};
	}
	
	$ctrl.alertteste= function () {
		alert('Parcelas geradas');
	}
		
}).controller('ModalParcelasController', function ($scope, $window, $uibModalInstance, demanda, CommonsService){
	var $ctrl = this;
	
	$ctrl.total_orcamento = demanda.orcamento.total_orcamento;
	
	$ctrl.calcularvalorrestante = function () {
		
		var valortotal = 0;
		for (var i in $ctrl.parcelas){
			var parcela = $ctrl.parcelas[i];
			if (!parcela.remover){
				valortotal += CommonsService.stringparafloat(parcela.valor_parcela);
			}
		}
		
		var valor_restante = CommonsService.stringparafloat($ctrl.total_orcamento) - valortotal;
		$ctrl.valor_restante = CommonsService.formatarnumero(valor_restante);
	}
	
	$ctrl.remover = function (i, callback){
		i.remover = true;		
		if (callback){
			callback();
		}
	}
	
	$ctrl.gerarparcelas = function (){
		
		$ctrl.parcelas = [];
		
		if (demanda.orcamento.total_orcamento && $ctrl.numero_vezes){
			var valorparcela = parseFloat(CommonsService.arrendodar(CommonsService.stringparafloat(demanda.orcamento.total_orcamento) / $ctrl.numero_vezes));
			
			var valortotal = 0;
			
			for (var int = 0; int < $ctrl.numero_vezes; int++) {
				var parcela = {
					descricao: (int + 1) + '/' + $ctrl.numero_vezes,
					valor_parcela: CommonsService.formatarnumero(valorparcela),
					status: 'PE'
				}
				valortotal+=valorparcela;
				$ctrl.parcelas.push(parcela);
			}
			
			var diferenca = CommonsService.stringparafloat(demanda.orcamento.total_orcamento) - valortotal;
			diferenca = CommonsService.stringparafloat($ctrl.parcelas[$ctrl.parcelas.length-1].valor_parcela) + diferenca;
			$ctrl.parcelas[$ctrl.parcelas.length-1].valor_parcela = CommonsService.formatarnumero(diferenca);
			
			$ctrl.calcularvalorrestante();
			
		}
	}
	
	$ctrl.adicionarparcela = function () {
		$ctrl.parcelas.push({});
	}
	
	$ctrl.fechar = function (){
		$uibModalInstance.close()	
	}
	
});
