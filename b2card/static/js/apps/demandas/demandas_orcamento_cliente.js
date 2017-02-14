"use strict";

demandas.controller('OrcamentoClienteController', function($rootScope, ValorHoraService, $uibModal, FaseService, CommonsService, share){
	var $ctrl = this;
	$ctrl.share = share;
	
	$ctrl.listafases = FaseService.buscarfases();
	$ctrl.listavalorhorab2card = ValorHoraService.buscarvalorhorab2card();
	
	
	$rootScope.$on('orcamentovalorhora', function (evt, data) {
		if (share.listavalorhora.$promise) {
			share.listavalorhora.$promise.then(function (data) {
				if ($ctrl.listavalorhorab2card.$promise){
					$ctrl.listavalorhorab2card.$promise.then(function (data) {
						$rootScope.$emit('calculardesejado');
						$rootScope.$emit('calcularprojetado');
						$rootScope.$emit('calcularproposto');
						$rootScope.$emit('incluirfasesorcamento');		
					});
				}
			});
		}	
	});
	
	$rootScope.$on('orcamento', function(event, data) {
		if (data.orcamento){
			
			data.orcamento.total_orcamento = CommonsService.formatarnumero(data.orcamento.total_orcamento);
			
			if (data.orcamento.orcamento_fases) {
				
				for (var fase of data.orcamento.orcamento_fases){
					if (fase.itensfase) {
						fase.valor_total = CommonsService.formatarnumero(fase.valor_total);
						for (var itemfase of fase.itensfase) {
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
	
	$ctrl.adicionaritemfase = function (orcamento_fase){
		if (!orcamento_fase.itensfase){
			orcamento_fase.itensfase = [];
		}
		orcamento_fase.itensfase.push({});
	}
	
	$ctrl.calcularvalortotalorcamento = () => {
		
		var fases = $ctrl.share.demanda.orcamento.orcamento_fases;
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
	
	$ctrl.changefasequantidadehoras = function (itemfase, orcamento_fase) {
		
		if (!itemfase.valor_hora || !itemfase.valor_hora.id){
			return;
		}
		
		for (var i in $ctrl.share.listavalorhora){
			var valorhora = $ctrl.share.listavalorhora[i]
			if (valorhora.id == itemfase.valor_hora.id){
				itemfase.valor_total  = CommonsService.formatarnumero((valorhora.vigencia ? valorhora.vigencia.valor : 0) * ( itemfase.quantidade_horas ? itemfase.quantidade_horas : 0));
			}
		}
		
		var itensfase = orcamento_fase.itensfase;
		
		var valorfase = 0
		for (i in itensfase){
			var itemfase = itensfase[i];
			if (!itemfase.remover && itemfase.valor_total) {
				var valoritem = CommonsService.stringparafloat(itemfase.valor_total);
				valorfase+=valoritem;
			}
		}
		
		orcamento_fase.valor_total = CommonsService.formatarnumero(valorfase);
		
		$ctrl.calcularvalortotalorcamento();
		
	}
	
	$ctrl.changevalorhora = function (itemfase, orcamento_fase) {
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
		$ctrl.changefasequantidadehoras(itemfase, orcamento_fase);
	}
	
	$ctrl.removeritemfase = function (i, orcamento_fase){
		i.remover = true;		
		$ctrl.changefasequantidadehoras(i, orcamento_fase);
	}
	
	$ctrl.remover = function (i, callback){
		i.remover = true;		
		if (callback){
			callback();
		}
	}
	
	$ctrl.abrirfecharmodaldespesas = () => {
		$ctrl.modaldespesasextras = !$ctrl.modaldespesasextras;
	}
	
	
	let buscarvalorhora = valor_hora_id => {
	
		if ($ctrl.listavalorhorab2card) {
			for (let valor_hora of $ctrl.listavalorhorab2card) {
				if (valor_hora.id == valor_hora_id) {
					return valor_hora;
				}
			}
		}
		
		if ($ctrl.share.listavalorhora) {
			for (let valor_hora of $ctrl.share.listavalorhora) {
				if (valor_hora.id == valor_hora_id) {
					return valor_hora;
				}
			}
		}
		
		return null;
		
	}
	
	let calcularatividadestotaishoras = () => {
		
		let horas_total = 0;
		
		if ($ctrl.share.demanda.orcamento.orcamento_fases) {
			for (let orcamento_fase of $ctrl.share.demanda.orcamento.orcamento_fases) {
				if (orcamento_fase.itensfase) {
					for(let item_fase of orcamento_fase.itensfase) {
						let valor_hora = buscarvalorhora(item_fase.valor_hora.id);
						horas_total+= item_fase.quantidade_horas;
					}
				}
			}
		}
		
		return horas_total;
	}
	
	let calcularatividadestotais = () => {
		
		let valor_total = 0;
		
		if ($ctrl.share.demanda.orcamento.orcamento_fases) {
			for (let orcamento_fase of $ctrl.share.demanda.orcamento.orcamento_fases) {
				if (orcamento_fase.itensfase) {
					for(let item_fase of orcamento_fase.itensfase) {
						let valor_hora = buscarvalorhora(item_fase.valor_hora.id);
						valor_total+=(item_fase.quantidade_horas * valor_hora.vigencia.valor);
					}
				}
			}
		}
		
		return valor_total;
	}
	
	$rootScope.$on('calculardesejado', function (event, data) {

		let valor_total = calcularatividadestotais();
		let custo_sem_imposto = valor_total * (1 + ($ctrl.share.demanda.orcamento.margem_risco / 100))
		
		if ($ctrl.share.demanda.orcamento.lucro_desejado && $ctrl.share.demanda.orcamento.imposto_devidos) {

			$ctrl.share.demanda.orcamento.valor_desejado = custo_sem_imposto / (($ctrl.share.demanda.orcamento.lucro_desejado / 100) + ($ctrl.share.demanda.orcamento.imposto_devidos / 100)) + CommonsService.stringparafloat($ctrl.share.demanda.orcamento.total_despesas ? $ctrl.share.demanda.orcamento.total_despesas : 0);
			
			if ($ctrl.share.demanda.orcamento.valor_hora_orcamento && $ctrl.share.demanda.orcamento.valor_hora_orcamento.id){
				let valor_hora = buscarvalorhora($ctrl.share.demanda.orcamento.valor_hora_orcamento.id);
				$ctrl.share.demanda.orcamento.horas_desejado =  ($ctrl.share.demanda.orcamento.valor_desejado / valor_hora.vigencia.valor).toFixed(2);
			}
			
			if ($ctrl.share.demanda.orcamento.valor_desejado) {
				$ctrl.share.demanda.orcamento.lucro_calculado_desejado = ((($ctrl.share.demanda.orcamento.valor_desejado - custo_sem_imposto - ($ctrl.share.demanda.orcamento.valor_desejado * ($ctrl.share.demanda.orcamento.imposto_devidos / 100))) / $ctrl.share.demanda.orcamento.valor_desejado) * 100).toFixed(2);
			}
			
			$ctrl.share.demanda.orcamento.valor_desejado = CommonsService.formatarnumero($ctrl.share.demanda.orcamento.valor_desejado)
		
		}
		
	});
	
	$rootScope.$on('calcularprojetado', function (event, data){
		
		let valor_total = calcularatividadestotais();
		let custo_sem_imposto = valor_total * (1 + ($ctrl.share.demanda.orcamento.margem_risco / 100))
		
		if ($ctrl.share.demanda.orcamento.valor_hora_orcamento && $ctrl.share.demanda.orcamento.valor_hora_orcamento.id) {
			let valor_hora = buscarvalorhora($ctrl.share.demanda.orcamento.valor_hora_orcamento.id);
			$ctrl.share.demanda.orcamento.valor_projetado = (valor_hora.vigencia.valor * $ctrl.share.demanda.orcamento.horas_projetadas) + CommonsService.stringparafloat($ctrl.share.demanda.orcamento.total_despesas ? $ctrl.share.demanda.orcamento.total_despesas : 0);
			
			if ($ctrl.share.demanda.orcamento.valor_projetado) {
				$ctrl.share.demanda.orcamento.lucro_calculado_projetado = ((($ctrl.share.demanda.orcamento.valor_projetado - custo_sem_imposto - ($ctrl.share.demanda.orcamento.valor_projetado * ($ctrl.share.demanda.orcamento.imposto_devidos / 100))) / $ctrl.share.demanda.orcamento.valor_projetado) * 100).toFixed(2);
			}
			
			$ctrl.share.demanda.orcamento.valor_projetado = CommonsService.formatarnumero($ctrl.share.demanda.orcamento.valor_projetado);
		}
	});
	
	$rootScope.$on('calcularproposto', function(event, data) {
		
		let valor_total = calcularatividadestotais();
		let custo_sem_imposto = valor_total * (1 + ($ctrl.share.demanda.orcamento.margem_risco / 100))
		
		let horas_total = calcularatividadestotaishoras()
		
		$ctrl.share.demanda.orcamento.valor_proposto = valor_total;
		$ctrl.share.demanda.orcamento.horas_proposto = horas_total;
		
		if ($ctrl.share.demanda.orcamento.valor_proposto) {
			$ctrl.share.demanda.orcamento.lucro_calculado_proposto = ((($ctrl.share.demanda.orcamento.valor_proposto - custo_sem_imposto - ($ctrl.share.demanda.orcamento.valor_proposto * ($ctrl.share.demanda.orcamento.imposto_devidos / 100))) / $ctrl.share.demanda.orcamento.valor_proposto) * 100).toFixed(2);
		}
		
		$ctrl.share.demanda.orcamento.valor_proposto = CommonsService.formatarnumero($ctrl.share.demanda.orcamento.valor_proposto);
		
	});
	
	$rootScope.$on('incluirfasesorcamento', function(event, data) {
		if (!$ctrl.share.demanda.orcamento.orcamento_fases || $ctrl.share.demanda.orcamento.orcamento_fases.length <= 0) {
			
			$ctrl.share.demanda.orcamento.orcamento_fases = [];
			var listfases = [];
			
			for (let orcamento_atividade of $ctrl.share.demanda.orcamento.orcamento_atividades) {
				if (orcamento_atividade.fase && listfases.indexOf(orcamento_atividade.fase.id) < 0) {
					$ctrl.share.demanda.orcamento.orcamento_fases.push({
						fase: orcamento_atividade.fase
					});
					listfases.push(orcamento_atividade.fase.id);
				}
			}
		}
	});
	
	$ctrl.alteracaoorcamento = () => {
		$rootScope.$emit('calculardesejado');
		$rootScope.$emit('calcularprojetado');
		$rootScope.$emit('calcularproposto');
	}
	
}).controller('ModalDespesasOrcamentoController', function ($rootScope, $scope, $window, share, CommonsService){
	var $ctrl = this;
	$ctrl.share = share;
	
	$ctrl.adicionardespesa = () => {
		if (!$ctrl.share.demanda.orcamento.despesas){
			$ctrl.share.demanda.orcamento.despesas = [];
		}
		
		$ctrl.share.demanda.orcamento.despesas.push({});
	}
	
	$ctrl.calculartotaldespesas = () => {
		if (!$ctrl.share.demanda.orcamento) {
			$ctrl.share.demanda.orcamento = {}	
		}

		// TODO buscar do banco em UN		
		$ctrl.share.demanda.orcamento.imposto_devidos= 20	
		
		if ($ctrl.share.demanda.orcamento.despesas){

			let total_despesas = 0;
			for (let despesa of $ctrl.share.demanda.orcamento.despesas) {
				if (despesa.descricao && despesa.valor){
					let valor = CommonsService.stringparafloat(despesa.valor);
					if (despesa.a_faturar) {
						valor = valor + (valor * ($ctrl.share.demanda.orcamento.imposto_devidos / 100));
					}
					total_despesas+=valor;
				}
			}
			
			$ctrl.share.demanda.orcamento.total_despesas = CommonsService.formatarnumero(parseFloat(total_despesas));
			
		}
		
		$rootScope.$emit('calculardesejado');
		$rootScope.$emit('calcularprojetado');
		$rootScope.$emit('calcularproposto');
		
	}
	
	
	
});