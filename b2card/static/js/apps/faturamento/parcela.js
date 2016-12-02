"use strict";

//var faturamento = angular.module('faturamento', ['commons', 'ui.bootstrap', 'ui.mask', 'demandas', 'parcela-services']);

demandas.controller('ModalParcelasController', function ($scope, $window, $uibModalInstance, demanda, CommonsService, ParcelaService){
	var $ctrl = this;
	
	$ctrl.total_orcamento = demanda.orcamento.total_orcamento;
	ParcelaService.buscartotalhoras(demanda.id, function (data){
		$ctrl.total_horas = data.total_horas
	});
	
	$ctrl.calcularvalorrestante = function () {
		
		var valortotal = 0;
		for (var i in $ctrl.parcelas){
			var parcela = $ctrl.parcelas[i];
			if (!parcela.remover && parcela.valor_parcela){
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
				
				var numero_horas = (valorparcela * $ctrl.total_horas) / CommonsService.stringparafloat($ctrl.total_orcamento);
				
				var parcela = {
					descricao: (int + 1) + '/' + $ctrl.numero_vezes,
					valor_parcela: CommonsService.formatarnumero(valorparcela),
					numero_horas : numero_horas,
					status: 'PE',
					demanda: demanda
				}
				valortotal+=valorparcela;
				$ctrl.parcelas.push(parcela);
			}
			
			var diferenca = CommonsService.stringparafloat(demanda.orcamento.total_orcamento) - valortotal;
			diferenca = CommonsService.stringparafloat($ctrl.parcelas[$ctrl.parcelas.length-1].valor_parcela) + diferenca;
			
			var numero_horas = (diferenca * $ctrl.total_horas) / CommonsService.stringparafloat($ctrl.total_orcamento);
			
			$ctrl.parcelas[$ctrl.parcelas.length-1].valor_parcela = CommonsService.formatarnumero(diferenca);
			$ctrl.parcelas[$ctrl.parcelas.length-1].numero_horas = numero_horas;
			
			$ctrl.calcularvalorrestante();
			
		}
	}
	
	$ctrl.gravarparcelas = function () {
		ParcelaService.gravarparcelas($ctrl.parcelas, function (data){
			$ctrl.parcelas = data;
			$window.alert('Parcelas geradas com sucesso!');
			$uibModalInstance.close($ctrl.parcelas);	
		});
	}
	
	$ctrl.changehoras = function () {
		
		for (var int = 0; int < $ctrl.parcelas.length; int++) {
			var parcela = $ctrl.parcelas[int];
			parcela.valor_parcela = CommonsService.formatarnumero(parcela.numero_horas * CommonsService.stringparafloat($ctrl.total_orcamento) / $ctrl.total_horas);
		}
		
		$ctrl.calcularvalorrestante();
		
	}
	
	$ctrl.adicionarparcela = function () {
		if (!$ctrl.parcelas){
			$ctrl.parcelas = [];
		}
		$ctrl.parcelas.push({
			status: 'PE',
			demanda: demanda
		});
	}
	
	$ctrl.fechar = function (){
		$uibModalInstance.close()	
	}
	
});
