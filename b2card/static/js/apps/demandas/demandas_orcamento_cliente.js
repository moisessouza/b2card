"use strict";

demandas.controller('OrcamentoClienteController', function($rootScope, ValorHoraService, $uibModal, FaseService, CommonsService, share){
	var $ctrl = this;
	$ctrl.share = share;
	
	$ctrl.listafases = FaseService.buscarfases();
		
	$rootScope.$on('orcamento', function(event, data) {
		if (data.orcamento){
			
			data.orcamento.total_orcamento = CommonsService.formatarnumero(data.orcamento.total_orcamento);
			
			if (data.orcamento.fases) {
				
				for (var i in data.orcamento.fases){
					
					var fase =  data.orcamento.fases[i]
					fase.valor_total = CommonsService.formatarnumero(fase.valor_total);
					
					if (fase.itensfase) {
						for (var j in fase.itensfase) {
							var itemfase = fase.itensfase[j]
							itemfase.valor_selecionado = CommonsService.formatarnumero(itemfase.valor_selecionado);
							itemfase.valor_total = CommonsService.formatarnumero(itemfase.valor_total);
						}
					}
				}
			}				
		}
	});
	
	$ctrl.modalprevisaofaturamento = function (){
		var modalInstance = $uibModal.open({
			animation : $ctrl.animationsEnabled,
			ariaLabelledBy : 'modal-title',
			ariaDescribedBy : 'modal-body',
			templateUrl : '/static/modal/modalContasReceber.html?bust=' + Math.random().toString(36).slice(2),
			controller : 'ModalParcelasController',
			controllerAs : '$ctrl',
			//size : 'lg'
			windowClass: 'app-modal-window',
			resolve : {
				demanda : function() {
					return share.demanda;
				},
				listavalorhora: function () {
					return share.listavalorhora;
				}
				
			}
		});
			
		modalInstance.result.then(function(data) {
			configurardemanda(share.demanda.id);
		}, function() {
			// $log.info('Modal dismissed at: ' + new Date());
		});
	}

	if ($ctrl.share.demanda.$promise) {
		$ctrl.share.demanda.$promise.then(function (data) {
			$rootScope.$emit('orcamento', data);
		});
	} 
	
	$ctrl.novafase = function () {
		$ctrl.fase = {
			itensfase: [{}]
		};
	}
	
	$ctrl.cancelarfase = function () {
		$ctrl.fase = null;
	}
	
	$ctrl.editarfase = function (fase) {
		$ctrl.fase = fase;
	}
	
	$ctrl.salvarfase = function () {
		if (!$ctrl.share.demanda.orcamento){
			$ctrl.share.demanda.orcamento = {};
		}
		if (!$ctrl.share.demanda.orcamento.fases){
			$ctrl.share.demanda.orcamento.fases = [];
		}
		
		if ($ctrl.fase.descricao){
			
			if ( $ctrl.fase.itensfase){
				for (var i in $ctrl.fase.itensfase){
					var itemfase = $ctrl.fase.itensfase[i];
					for (var j in $ctrl.share.listavalorhora){
				
						var valorhora = $ctrl.share.listavalorhora[j];
						if (itemfase.valor_hora && valorhora.id == itemfase.valor_hora.id){
							itemfase.valor_hora.descricao = valorhora.descricao;
							break;
						}
					}
					
				}
			}
			
			if ($ctrl.share.demanda.orcamento.fases.indexOf($ctrl.fase) < 0){
				$ctrl.share.demanda.orcamento.fases.push($ctrl.fase);	
			}
		}
		
		$ctrl.fase = null;
		
		$ctrl.calcularvalortotalorcamento();
	}
	
	$ctrl.adicionaritemfase = function (){
		if (!$ctrl.fase.itensfase){
			$ctrl.fase.itensfase = [];
		}
		$ctrl.fase.itensfase.push({});
	}
	
	$ctrl.calcularvalortotalorcamento = function (){
		
		var fases = $ctrl.share.demanda.orcamento.fases;
		var totalorcamento = 0;
		
		for (var i in fases) {
			var fase = fases[i];
			if (!fase.remover) {
				var itensfase = fase.itensfase;
				
				var valorfase = 0
				for (i in itensfase){
					var itemfase = itensfase[i];
					if (!itemfase.remover && itemfase.valor_total) {
						var valoritem = CommonsService.stringparafloat(itemfase.valor_total);
						valorfase+=valoritem;
					}
				}
				
				fase.valor_total = CommonsService.formatarnumero(valorfase);
				totalorcamento+= valorfase;
			}
		}
		
		$ctrl.share.demanda.orcamento.total_orcamento =  CommonsService.formatarnumero(totalorcamento);
	}
	
	$ctrl.changefasequantidadehoras = function (itemfase) {
		for (var i in $ctrl.share.listavalorhora){
			var valorhora = $ctrl.share.listavalorhora[i]
			if (valorhora.id == itemfase.valor_hora.id){
				itemfase.valor_total  = CommonsService.formatarnumero((valorhora.vigencia ? valorhora.vigencia.valor : 0) * ( itemfase.quantidade_horas ? itemfase.quantidade_horas : 0));
			}
		}
		
		var itensfase = $ctrl.fase.itensfase;
		
		var valorfase = 0
		for (i in itensfase){
			var itemfase = itensfase[i];
			if (!itemfase.remover && itemfase.valor_total) {
				var valoritem = CommonsService.stringparafloat(itemfase.valor_total);
				valorfase+=valoritem;
			}
		}
		
		$ctrl.fase.valor_total = CommonsService.formatarnumero(valorfase);
		
		$ctrl.calcularvalortotalorcamento();
		
	}
	
	$ctrl.changevalorhora = function (itemfase) {
		itemfase.valor_selecionado = CommonsService.formatarnumero(0);
		for (var i in $ctrl.share.listavalorhora){
			var valorhora = $ctrl.share.listavalorhora[i]
			if (valorhora && valorhora.vigencia){
				if (valorhora.id == itemfase.valor_hora.id){
					itemfase.valor_selecionado = CommonsService.formatarnumero(valorhora.vigencia && valorhora.vigencia.valor ? valorhora.vigencia.valor : 0);
					break;
				}
			}
		}
		$ctrl.changefasequantidadehoras(itemfase);
	}
	
	$ctrl.remover = function (i, callback){
		i.remover = true;		
		if (callback){
			callback();
		}
	}
	
});