var demandas = angular.module('demandas', ['demandas-services',  'ui.bootstrap']);

demandas.controller('DemandaController', function ($scope, $uibModal, $log, DemandaService){
	$ctrl = this; 
	$scope.demanda = {
		proposta: [
			{
				numero_proposta: '123456',
				data_proposta: '21/12/2015',
				eh_corrente: false
			},
		    {
		    	numero_proposta: '123456',
		    	data_proposta: '21/12/2016',
		    	eh_corrente: true
			}
		]
	}
	
	$scope.listaclientes= DemandaService.buscarclientes();
	$scope.listacoordenador = DemandaService.buscarfuncionarios();
	
	$scope.open = function (size, parentSelector) {
	    var parentElem = parentSelector ? 
	      angular.element($document[0].querySelector('.modal-demo ' + parentSelector)) : undefined;
	    var modalInstance = $uibModal.open({
	      animation: $ctrl.animationsEnabled,
	      ariaLabelledBy: 'modal-title',
	      ariaDescribedBy: 'modal-body',
	      templateUrl: 'myModalContent.html',
	      controller: 'ModalInstanceCtrl',
	      controllerAs: '$ctrl',
	      size: size,
	      appendTo: parentElem,
	      resolve: {
	        demanda: function () {
	          return $scope.demanda;
	        }
	      }
	    });
	    
	    modalInstance.result.then(function (proposta) {
	        console.log(proposta);
	      }, function () {
	        $log.info('Modal dismissed at: ' + new Date());
	      });
	};	
	
});

demandas.controller('ModalInstanceCtrl', function ($uibModalInstance, demanda) {
	  var $ctrl = this;
	  $ctrl.demanda = demanda;
	  	
	  $ctrl.ok = function () {
		  
		  for ( index in $ctrl.demanda.proposta ){
			  $ctrl.demanda.proposta[index].eh_corrente=false;
		  }		  
		  
		  $ctrl.proposta.eh_corrente=true;
		  $ctrl.demanda.proposta.push($ctrl.proposta);
		  $uibModalInstance.close($ctrl.proposta);
	  };
	
	  $ctrl.cancel = function () {
	    $uibModalInstance.dismiss('cancel');
	  };
});