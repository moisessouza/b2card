var demandas = angular.module('demandas', ['demandas-services', 'commons', 'ui.bootstrap']);

demandas.controller('DemandaController', function ($scope, $uibModal, $log, DemandaService, CommonsService){
	var $ctrl = this; 
	$ctrl.demanda = {
		'itens_faturamento': []
	}
	
	$ctrl.adicionaritem = function () {
		$ctrl.demanda.itens_faturamento.push({});
	}
	
	$ctrl.listaclientes= DemandaService.buscarclientes();
	$ctrl.listacoordenador = DemandaService.buscarfuncionarios();
	
	$ctrl.changecliente = function (){
		$ctrl.listatipovalorhora  = DemandaService.buscartipohoracliente($ctrl.demanda.cliente.id);	
	}
	
	$ctrl.changehoraproposta = function (item_faturamento) {
		if (item_faturamento.tipo_horas){
			var tipo_horas = item_faturamento.tipo_horas;
			var valor_hora = parseFloat(tipo_horas.valor_hora.replace('.', '').replace(',','.'));
			item_faturamento.valor_hora = tipo_horas.valor_hora;
			var valor_faturamento = valor_hora * (item_faturamento.quantidade_horas ? item_faturamento.quantidade_horas : 0);
			item_faturamento.valor_faturamento = CommonsService.formatarnumero(valor_faturamento);
		}
	}
	
});