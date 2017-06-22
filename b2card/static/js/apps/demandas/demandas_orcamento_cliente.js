"use strict";

demandas.controller('OrcamentoClienteController', function($rootScope, $window, ValorHoraService, $uibModal, FaseService, CommonsService, share){
	var $ctrl = this;
	$ctrl.share = share;
	
	$ctrl.valorhoraporfasemap = {}
	
	let data = share.demanda.data_criacao ? share.demanda.data_criacao : new Date();
	data = CommonsService.dataparaurl(data);
	$ctrl.listavalorhorab2card = ValorHoraService.buscarvalorhorab2card(data);
	
	$ctrl.listavalortaxab2card = ValorHoraService.buscarvalortaxab2card(data);
	
	$rootScope.$on('orcamentovalorhora', function (evt) {
		
		let data = share.demanda.data_criacao ? share.demanda.data_criacao : new Date();
		data = CommonsService.dataparaurl(data);
		$ctrl.listavalorhorab2card = ValorHoraService.buscarvalorhorab2card(data);
	
		$ctrl.listavalorhorab2card = ValorHoraService.buscarvalorhorab2card(data, function (data){
			if (share.listavalorhora.$promise) {
				// - busca valor % de lucro e margem de risco no cadastro de horas - Nilson
				if ($ctrl.share.demanda.orcamento.lucro_desejado == null) {
					if (share.listavalorhora) {
						for (let valorlucro of share.listavalorhora) {
							if ((valorlucro.centro_resultado.nome == 'B2Card' && valorlucro.descricao == 'Valor % Lucro')) {
								$ctrl.share.demanda.orcamento.lucro_desejado = valorlucro.vigencia.valor; 
							}
						}
					}					
				}
				if ($ctrl.share.demanda.orcamento.margem_risco == null) {
					if (share.listavalorhora) {
						for (let valormargemrisco of share.listavalorhora) {
							if ((valormargemrisco.centro_resultado.nome == 'B2Card' && valormargemrisco.descricao == 'Valor % Margem Risco')) {
								$ctrl.share.demanda.orcamento.margem_risco = valormargemrisco.vigencia.valor;
							}
						}
					}
				}	
				// -#				
				
				share.listavalorhora.$promise.then(function (data) {
					if ($ctrl.listavalorhorab2card.$promise){
						$ctrl.listavalorhorab2card.$promise.then(function (data) {
							$rootScope.$emit('calculardesejado');
							$rootScope.$emit('calcularprojetado');
							$rootScope.$emit('calcularproposto');
							$rootScope.$emit('incluirfasesorcamento');		
						});
					}
	
					
					if (!$ctrl.listafases){
						$ctrl.listafases = FaseService.buscarfases();
					}

					if ($ctrl.listafases.$promise){
						$ctrl.listafases.$promise.then(function (data) {
							if ($ctrl.share.listavalorhora) {
								for (let fase of data) {
									$ctrl.valorhoraporfasemap[fase.id] = [];
									for (let valorhora of $ctrl.share.listavalorhora){
										if (fase.centro_resultado && valorhora.centro_resultado) {
											if (fase.centro_resultado.id == valorhora.centro_resultado.id){
												$ctrl.valorhoraporfasemap[fase.id].push(valorhora);
											}
										}
									}
								}
							}
						});
					}
					
				});
			}
		});
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
	
	$ctrl.gerararquivoproposta = () => {
		$window.open(BASE_URL + 'faturamento/gerar_arquivo_faturamento/' + share.demanda.id, '_blank');
	}
	
	$ctrl.gerararquivopropostaorcamento = () => {
		$window.open(BASE_URL + 'faturamento/gerar_arquivo_faturamento_comercial/' + share.demanda.id, '_blank');
	}
	
	$ctrl.modalprevisaofaturamento = function (){
		var modalInstance = $uibModal.open({
			animation : $ctrl.animationsEnabled,
			ariaLabelledBy : 'modal-title',
			ariaDescribedBy : 'modal-body',
			templateUrl : '/static/modal/modalItensFaturamento.html?bust=' + Math.random().toString(36).slice(2),
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
				},
				lote_faturamento : false,
				listaitensfaturamento: function () {
					return [];
				}
			}
		});
			
		modalInstance.result.then(function(data) {
			// configurardemanda(share.demanda.id);
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
	
// - busca valor imposto e custo administrativo no cadastro de horas - Nilson

	let buscarvalorimposto = idtaxa_id => {
		var valor_imposto = null;
		if ($ctrl.listavalortaxab2card) {
			for (let valor_imp of $ctrl.listavalortaxab2card) {
				if ((valor_imp.centro_resultado.nome == idtaxa_id && valor_imp.centro_custo.nome == idtaxa_id && valor_imp.descricao == 'Valor % Impostos')) {
					valor_imposto = valor_imp.vigencia.valor;
				}
			}
			return valor_imposto;
		}
		return null;
	}
	
	let buscarvalorcustoadmin = idtaxa_id => {
		
		var valor_custoad = null;
		if ($ctrl.listavalortaxab2card) {
			for (let valor_cadm of $ctrl.listavalortaxab2card) {
				if ((valor_cadm.centro_resultado.nome == idtaxa_id && valor_cadm.centro_custo.nome == idtaxa_id && valor_cadm.descricao == 'Valor % Custo Administrativo')) {
					valor_custoad = valor_cadm.vigencia.valor;
				}
			}
			return valor_custoad;
		}
		return null;
	}	
	
//  	
	
	let calcularatividadestotaishoras = () => {
		
		let coluna_valor_map = {};
		
		if ($ctrl.share.demanda.orcamento.orcamento_atividades) {
			for (let orcamento_atividade of $ctrl.share.demanda.orcamento.orcamento_atividades) {
				if (orcamento_atividade.colunas){
					for (let coluna in orcamento_atividade.colunas){
						let valor_hora = buscarvalorhora(coluna);
						if (coluna_valor_map[valor_hora.id]) {
							coluna_valor_map[valor_hora.id] += orcamento_atividade.colunas[valor_hora.id].horas; 
						} else {
							coluna_valor_map[valor_hora.id] = orcamento_atividade.colunas[valor_hora.id].horas; 
						}
					}
				}
			}
			
		}
		
		let horas_total = 0;
		
		for (let coluna in coluna_valor_map) {
			horas_total+=coluna_valor_map[coluna];
		}
		
		return horas_total;
	}
	
	let calcularatividadestotais = () => {
		
		let coluna_valor_map = {};
		
		if ($ctrl.share.demanda.orcamento.orcamento_atividades) {
			for (let orcamento_atividade of $ctrl.share.demanda.orcamento.orcamento_atividades) {
				if (orcamento_atividade.colunas){
					for (let coluna in orcamento_atividade.colunas){
						let valor_hora = buscarvalorhora(coluna);
						if (coluna_valor_map[valor_hora.id]) {
							coluna_valor_map[valor_hora.id] += orcamento_atividade.colunas[valor_hora.id].horas * valor_hora.vigencia.valor; 
						} else {
							coluna_valor_map[valor_hora.id] = orcamento_atividade.colunas[valor_hora.id].horas * valor_hora.vigencia.valor; 
						}
					}
				}
			}
			
		}
		
		let valor_total = 0;
		
		for (let coluna in coluna_valor_map) {
			valor_total+=coluna_valor_map[coluna];
		}
		
		return valor_total;
	}
	
	var calcularcustooperacional = function () {
		let unidadeadministrativa = null;
		
		if ($ctrl.share.demanda.unidade_administrativa){
			if ($ctrl.share.listaunidadeadministrativas){
				for(let u of $ctrl.share.listaunidadeadministrativas) {
					if (u.id == $ctrl.share.demanda.unidade_administrativa.id) {
						unidadeadministrativa = u;
						break;
					}
				}
			}
		}
		
		let horas_totais = calcularatividadestotaishoras();
		return (horas_totais + (horas_totais * ($ctrl.share.demanda.orcamento.margem_risco / 100))) * (unidadeadministrativa ? unidadeadministrativa.custo_operacao_hora : 0);
	};

	
	// - Novo calculo para custo operacional - Nilson - 
	var calcularcustooperacionalnew = function () {
		let unidadeadministrativanew = null;
		
		if ($ctrl.share.demanda.unidade_administrativa){
			if ($ctrl.share.listaunidadeadministrativas){
				for(let un of $ctrl.share.listaunidadeadministrativas) {
					if (un.id == $ctrl.share.demanda.unidade_administrativa.id) {
						unidadeadministrativanew = un;
						break;
					}
				}
			}
		}
		
		let horas_totaisnew = calcularatividadestotaishoras();
		return (horas_totaisnew);
	};	
	
	var calcularcustosemimposto = function (valor_total) {
	    let custo_operacional = calcularcustooperacional();
		return (valor_total * (1 + ($ctrl.share.demanda.orcamento.margem_risco / 100)))  + custo_operacional;
	};
	

	// - Novo calculo para custo total sem imposto - Nilson - 
	var calcularcustosemimpostonovo = function (valor_total) {
		let custo_operacionalnew = calcularcustooperacionalnew();
		return (valor_total * (1 + ($ctrl.share.demanda.orcamento.margem_risco / 100)));
	};	
	
	$rootScope.$on('calculardesejado', function (event, data) {

		var grupodtaxa = 'B2Card';
		let valor_imposto = buscarvalorimposto(grupodtaxa);
		let valor_custo_admin = buscarvalorcustoadmin(grupodtaxa);
		$ctrl.share.valor_imposto = valor_imposto; 
		$ctrl.share.valor_custo_admin = valor_custo_admin;
		
		let valor_total = calcularatividadestotais();
	  //let custo_sem_imposto = calcularcustosemimposto(valor_total);
		let custo_sem_imposto = calcularcustosemimpostonovo(valor_total);

		if ($ctrl.share.valor_imposto == null){
			alert("\n                                !!!!!!       Atenção      !!!!!!\n\n - % Imposto - não encontrado no cadastro >Valor Hora< !");
			$ctrl.share.demanda.orcamento.valor_desejado = null;
			$ctrl.share.demanda.orcamento.horas_desejado = null;
			$ctrl.share.demanda.orcamento.lucro_calculado_desejado = null;
			return;
		}

		if ($ctrl.share.valor_custo_admin == null){
			alert("\n                                !!!!!!       Atenção      !!!!!!\n\n - % Margem Risco - não encontrado no cadastro >Valor Hora< !");
			$ctrl.share.demanda.orcamento.valor_desejado = null;
			$ctrl.share.demanda.orcamento.horas_desejado = null;
			$ctrl.share.demanda.orcamento.lucro_calculado_desejado = null;
			return;
		}
		
		//if (($ctrl.share.demanda.orcamento.lucro_desejado || $ctrl.share.demanda.orcamento.lucro_desejado == 0) && ($ctrl.share.demanda.orcamento.imposto_devidos || $ctrl.share.demanda.orcamento.imposto_devidos == 0)) {
		  if (($ctrl.share.demanda.orcamento.lucro_desejado || $ctrl.share.demanda.orcamento.lucro_desejado == 0) && ($ctrl.share.demanda.orcamento.imposto_devidos || $ctrl.share.demanda.orcamento.imposto_devidos == 0) && ($ctrl.share.valor_imposto || $ctrl.share.valor_imposto == 0) && ($ctrl.share.valor_custo_admin ||$ctrl.share.valor_custo_admin == 0)) {  
		  //$ctrl.share.demanda.orcamento.valor_desejado = (custo_sem_imposto / (1 - (($ctrl.share.demanda.orcamento.lucro_desejado / 100) + ($ctrl.share.demanda.orcamento.imposto_devidos / 100)))) + CommonsService.stringparafloat($ctrl.share.demanda.orcamento.total_despesas ? $ctrl.share.demanda.orcamento.total_despesas : 0);
			$ctrl.share.demanda.orcamento.valor_desejado = (custo_sem_imposto / (1 - ((($ctrl.share.valor_imposto + $ctrl.share.valor_custo_admin + $ctrl.share.demanda.orcamento.lucro_desejado) /100)))) + CommonsService.stringparafloat($ctrl.share.demanda.orcamento.total_despesas ? $ctrl.share.demanda.orcamento.total_despesas : 0);
			if ($ctrl.share.demanda.orcamento.valor_hora_orcamento && $ctrl.share.demanda.orcamento.valor_hora_orcamento.id){
				let valor_hora = buscarvalorhora($ctrl.share.demanda.orcamento.valor_hora_orcamento.id);
				$ctrl.share.demanda.orcamento.horas_desejado =  ($ctrl.share.demanda.orcamento.valor_desejado / valor_hora.vigencia.valor).toFixed(2);
			}
			if ($ctrl.share.demanda.orcamento.valor_desejado) {
			  //$ctrl.share.demanda.orcamento.lucro_calculado_desejado = ((($ctrl.share.demanda.orcamento.valor_desejado - custo_sem_imposto - ($ctrl.share.demanda.orcamento.valor_desejado * ($ctrl.share.demanda.orcamento.imposto_devidos / 100))) / $ctrl.share.demanda.orcamento.valor_desejado) * 100).toFixed(2);
				$ctrl.share.demanda.orcamento.lucro_calculado_desejado = ((($ctrl.share.demanda.orcamento.valor_desejado - custo_sem_imposto - ($ctrl.share.demanda.orcamento.valor_desejado * (($ctrl.share.valor_imposto + $ctrl.share.valor_custo_admin ) / 100))) / $ctrl.share.demanda.orcamento.valor_desejado) * 100).toFixed(2);
			}
			$ctrl.share.demanda.orcamento.valor_desejado = CommonsService.formatarnumero($ctrl.share.demanda.orcamento.valor_desejado)
		
		}
		
	});
	
	$rootScope.$on('calcularprojetado', function (event, data){

		var grupodtaxa = 'B2Card';
		let valor_total = calcularatividadestotais();
	  //let custo_sem_imposto = calcularcustosemimposto(valor_total);
		let custo_sem_imposto = calcularcustosemimpostonovo(valor_total);
		
		if ($ctrl.share.demanda.orcamento.valor_hora_orcamento && $ctrl.share.demanda.orcamento.valor_hora_orcamento.id) {
			let valor_hora = buscarvalorhora($ctrl.share.demanda.orcamento.valor_hora_orcamento.id);
			$ctrl.share.demanda.orcamento.valor_projetado = (valor_hora.vigencia.valor * $ctrl.share.demanda.orcamento.horas_projetadas) + CommonsService.stringparafloat($ctrl.share.demanda.orcamento.total_despesas ? $ctrl.share.demanda.orcamento.total_despesas : 0);
			
			if ($ctrl.share.demanda.orcamento.valor_projetado) {
			  //$ctrl.share.demanda.orcamento.lucro_calculado_projetado = ((($ctrl.share.demanda.orcamento.valor_projetado - custo_sem_imposto - ($ctrl.share.demanda.orcamento.valor_projetado * ($ctrl.share.demanda.orcamento.imposto_devidos / 100))) / $ctrl.share.demanda.orcamento.valor_projetado) * 100).toFixed(2);
				$ctrl.share.demanda.orcamento.lucro_calculado_projetado = ((($ctrl.share.demanda.orcamento.valor_projetado - custo_sem_imposto - ($ctrl.share.demanda.orcamento.valor_projetado * (($ctrl.share.valor_imposto + $ctrl.share.valor_custo_admin ) / 100)))/ $ctrl.share.demanda.orcamento.valor_projetado) * 100).toFixed(2);

			}
			
			$ctrl.share.demanda.orcamento.valor_projetado = CommonsService.formatarnumero($ctrl.share.demanda.orcamento.valor_projetado);
		}
	});
	
	
	let selecionarfaseorcamentostotais = () => {
		
		let valor_total = 0;
		
		if ($ctrl.share.demanda.orcamento.orcamento_fases) {
			for (let orcamento_fase of $ctrl.share.demanda.orcamento.orcamento_fases) {
				if (orcamento_fase.itensfase) {
					for (let item_fase of orcamento_fase.itensfase) {
						let valor_hora = buscarvalorhora(item_fase.valor_hora.id);
						valor_total+=(valor_hora.vigencia.valor * item_fase.quantidade_horas)
					}
				}
			}
		}
		
		return valor_total;
		
	}
	
	let selecionarfaseorcamentostotaishoras = () => {
		
		let horas_totais = 0;
		
		if ($ctrl.share.demanda.orcamento.orcamento_fases) {
			for (let orcamento_fase of $ctrl.share.demanda.orcamento.orcamento_fases) {
				if (orcamento_fase.itensfase) {
					for (let item_fase of orcamento_fase.itensfase) {
						horas_totais += item_fase.quantidade_horas;
					}
				}
			}
		}
		
		return horas_totais;
		
	}
	
	$rootScope.$on('calcularproposto', function(event, data) {

		var grupodtaxa = 'B2Card';
		
		let valor_total = selecionarfaseorcamentostotais();
	  //let custo_sem_imposto = calcularcustosemimposto(calcularatividadestotais());
		let custo_sem_imposto = calcularcustosemimpostonovo(calcularatividadestotais());
		let horas_total = selecionarfaseorcamentostotaishoras()
		
		$ctrl.share.demanda.orcamento.valor_proposto = valor_total;
		$ctrl.share.demanda.orcamento.horas_proposto = horas_total;
		
		if ($ctrl.share.demanda.orcamento.valor_proposto) {
		  //$ctrl.share.demanda.orcamento.lucro_calculado_proposto = ((($ctrl.share.demanda.orcamento.valor_proposto - custo_sem_imposto - ($ctrl.share.demanda.orcamento.valor_proposto * ($ctrl.share.demanda.orcamento.imposto_devidos / 100))) / $ctrl.share.demanda.orcamento.valor_proposto) * 100).toFixed(2);
			$ctrl.share.demanda.orcamento.lucro_calculado_proposto = ((($ctrl.share.demanda.orcamento.valor_proposto - custo_sem_imposto - ($ctrl.share.demanda.orcamento.valor_proposto * (($ctrl.share.valor_imposto + $ctrl.share.valor_custo_admin ) / 100))) / $ctrl.share.demanda.orcamento.valor_proposto) * 100).toFixed(2);

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
	
	$ctrl.recarregarfases = () => {
		if ($ctrl.share.demanda.orcamento.orcamento_fases) {
			for (let o of $ctrl.share.demanda.orcamento.orcamento_fases){
				o.remover = true;
			}
		}
		$rootScope.$emit('incluirfasesorcamento');
	}
	
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
		
		if ($ctrl.share.demanda.orcamento.despesas){
			
			let total_despesas = 0;
			for (let despesa of $ctrl.share.demanda.orcamento.despesas) {
				if (despesa.descricao && despesa.valor){
					let valor = CommonsService.stringparafloat(despesa.valor);
					if (despesa.a_faturar) {
					  //valor = valor + (valor * (20 / 100));
						valor = valor + (valor * ($ctrl.share.valor_imposto / 100));
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