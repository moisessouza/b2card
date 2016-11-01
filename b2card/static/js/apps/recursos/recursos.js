var recursos = angular.module('recursos', ['recursos-services', 'commons', 'ui.bootstrap']);

recursos.controller('RecursosController', function ($scope, $uibModal, $window, $location, RecursosService){
	var $ctrl = this;
	
	var messageinfo = function (msg){
		$ctrl.clazz = 'label-primary';	
		$ctrl.message = msg;
	}
	
	var messagesuccess = function (msg) {
		$ctrl.clazz = 'label-success';
		$ctrl.message = msg;
	}
	
	if (funcionario_id){
		$ctrl.funcionario = RecursosService.buscarfuncionario(funcionario_id);
	} else {
		$ctrl.funcionario = {};	
	}
	
	$ctrl.listacargos = RecursosService.buscarcargos();
	
	$scope.open = function (size, parentSelector) {
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
	
	$ctrl.salvar = function () {
		messageinfo("salvando...");
		RecursosService.salvarfuncionario($ctrl.funcionario, function (data){
			$ctrl.funcionario.id = data.id;
			messagesuccess('salvo!');
			
		});
	}
	
	$ctrl.deletar = function () {
		var confirm = $window.confirm("Tem certeza que deseja deletar esse funcionário?");
		if (confirm){
			RecursosService.deletarfuncionario($ctrl.funcionario.id, function (data){
				$window.location.href = '/recursos/';
			});
		}
	};
	
	
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
