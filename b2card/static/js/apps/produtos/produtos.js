var produtos = angular.module('produtos', ['ngResource',	'produtos-services']);

produtos.controller('ProdutoController', function ($scope, MateriaisService, ProdutoService){
	
		if (produto_id){
			ProdutoService.buscarproduto (produto_id, function (data){
				$scope.produto = data;
			})
		} else {
			$scope.produto = {
				'material_produto':[]
			};	
		}
		
		
		$scope.materiaislist = MateriaisService.buscarmateriais()
		
		$scope.addmaterial = function () {
			$scope.produto.material_produto.push({});
		};

		var calcularcusto = function () {
			var custototal = 0;
			
			for (m in $scope.materiaislist){
				for (mp in $scope.produto.material_produto){
					if ($scope.materiaislist[m].id == $scope.produto.material_produto[mp].material){
						custototal+= parseFloat($scope.materiaislist[m].preco.replace('.', '').replace(',', '.')) * $scope.produto.material_produto[mp].quantidade;
						break;
					}
				}
			}
			
			$scope.produto.custo_total = custototal;
			
		}
		
		$scope.changematerial = function (valor) {
			calcularcusto();		
		}
				
		$scope.gravar = function (){
			ProdutoService.salvarproduto($scope.produto, function (data){
				$scope.produto.id = data.id;
				alert('gravado');
			});
		};
		
});