"use strict";

var pessoa = angular.module('pessoa', ['pessoa-services', 'centrocusto-services', 'recursos-services', 'commons', 'ui.bootstrap', 'ui.mask']);

pessoa.controller('PessoaController', function ($scope, $window, $uibModal, PessoaService, CentroCustoService, MessageService, RecursosService){
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
	
	$ctrl.listacargos = RecursosService.buscarcargos();
	
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
	
	
	$ctrl.open = function (size, parentSelector) {
	    var modalInstance = $uibModal.open({
	      animation: $ctrl.animationsEnabled,
	      ariaLabelledBy: 'modal-title',
	      ariaDescribedBy: 'modal-body',
	      templateUrl: 'myModalContent.html',
	      controller: 'ModalInstanceCtrl',
	      controllerAs: '$ctrl',
	      size: size,
	      resolve: {
	        demanda: function () {
	          return $scope.demanda;
	        }
	      }
	    });
	    
	    modalInstance.result.then(function (proposta) {
	    	$ctrl.listacargos = RecursosService.buscarcargos();
	    }, function () {
	        //$log.info('Modal dismissed at: ' + new Date());
	    });
	};
	
}).controller('ListPessoaController', function ($scope, $window, PessoaService){
	var $ctrl = this;
	
	$ctrl.pessoas = PessoaService.buscarpessoas();
	
	$ctrl.redirecionar = function (pessoa) {
		$window.location.href = '/cadastros/pessoa/editar/' + pessoa.id
	}
	
}).controller('ModalInstanceCtrl', function($scope, $uibModalInstance, RecursosService){
	
	var $ctrl = this;
	
	$ctrl.listacargos = RecursosService.buscarcargos();
	
	$ctrl.salvar = function () {
		
		if (!$ctrl.cargo)
			$ctrl.cargo = {}
		
		$ctrl.cargo.nome_cargo = $ctrl.nome_cargo;
		RecursosService.salvarcargo($ctrl.cargo, function (data){
			if (!$ctrl.cargo.edit){
				$ctrl.listacargos.push(data);
			}
			$ctrl.cargo = {}
			$ctrl.nome_cargo = "";
		});
	}
	
	$ctrl.deletar = function () {
		RecursosService.deletarcargo($ctrl.cargo, function (data){
			$ctrl.listacargos.splice($ctrl.listacargos.indexOf($ctrl.cargo), 1);
			$ctrl.cargo = {}
			$ctrl.nome_cargo = "";
		});
	}
	
	$ctrl.deletar = function () {
		RecursosService.deletarcargo($ctrl.cargo, function (data){
			$ctrl.listacargos.splice($ctrl.listacargos.indexOf($ctrl.cargo), 1);
			$ctrl.cargo = {}
			$ctrl.nome_cargo = "";
		});
	}
	
	$ctrl.edit = function (cargo) {
		$ctrl.cargo = cargo;
		$ctrl.cargo.edit=true;
		$ctrl.nome_cargo = cargo.nome_cargo;
	}
	
	$ctrl.close = function () {
	   $uibModalInstance.close({});
	};
});