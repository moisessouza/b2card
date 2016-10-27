var demandas = angular.module('demandas', ['demandas-services']);

demandas.controller('DemandaController', function ($scope, DemandaService){

	$scope.listaclientes= DemandaService.buscarclientes();
	
});