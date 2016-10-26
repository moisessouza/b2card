var produtos = angular.module('orcamentos', ['ngResource', 'orcamentos-services', 'produtos-services']);

produtos.controller('OrcamentoController', function ($scope, ProdutoService, OrcamentosService){

	if (orcamento_id){
		$scope.orcamento = OrcamentosService.buscarorcamento(orcamento_id);
	} else {
		$scope.orcamento = {
			descricao:'',
			produtos:[],
			preco_final: ''
		}	
	}
	
	$scope.listaprodutos = ProdutoService.buscartodosprodutos();
	
	$scope.addprodutos = function () {
		$scope.orcamento.produtos.push({})
	};
	
	$scope.deletarmaterial = function (produto) {
		$scope.orcamento.produtos.splice($scope.orcamento.produtos.indexOf(produto), 1);
	};
	
	$scope.gravar = function () {
		OrcamentosService.salvar($scope.orcamento, function (data){
			$scope.orcamento.id = data.id;
			alert('Gravado!!!!');
		});
	};
	
});