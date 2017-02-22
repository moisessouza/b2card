"use strict";

var parcela = angular.module('parcela', ['valorhora-services', 'parcela-services', 'commons', 'ui.bootstrap', 'ui.mask']);

parcela.controller('ModalParcelasController', function ($scope, $window, $uibModalInstance, demanda, listavalorhora, lote_faturamento, listaitensfaturamento, CommonsService, ParcelaService){
	var $ctrl = this;
	
	$ctrl.demanda = demanda;
	$ctrl.total_orcamento = demanda.orcamento.total_orcamento;
	$ctrl.listavalorhora = listavalorhora;
	$ctrl.listafases = demanda.orcamento.orcamento_fases;
	$ctrl.lote_faturamento = lote_faturamento;
	
	var configurarparcelas = function (parcelas) {
		for ( var i in parcelas) {
			
			var parcela = parcelas[i];
			if (parcela.valor_parcela){
				parcela.valor_parcela =  CommonsService.formatarnumero(parcela.valor_parcela);
			}
			
			if (parcela.parcelafases){
				
				for (var pf = 0; pf < parcela.parcelafases.length; pf++) {
					var parcelafase = parcela.parcelafases[pf]
					
					if (parcelafase.medicoes && parcelafase.medicoes.length > 0){
						for (var m = 0; m < parcelafase.medicoes.length; m++) {
							var medicao = parcelafase.medicoes[m];
							if (medicao.valor_total){
								medicao.valor_total = CommonsService.formatarnumero(medicao.valor_total);
							}
						}
					} else if (parcelafase.valor) {
						parcelafase.valor = CommonsService.formatarnumero(parcelafase.valor);
					}
				
				}
			}
		}
	}
	
	ParcelaService.buscarlistavalorhoraporfase(demanda.id, function (data) {
		if (data){
			$ctrl.valorhoraobject = {}
			for (var int = 0; int < data.length; int++) {
				var o = data[int];
				$ctrl.valorhoraobject[o.id] = o.valorhora;
			}		
		}
	});
	
	ParcelaService.buscarparcelageradas(demanda.id, function (data){
		if (data) {
			$ctrl.parcelas = data;
			$ctrl.tipo = demanda.tipo_parcela;
			
			configurarparcelas($ctrl.parcelas);
			
			if (lote_faturamento && data) {
				for (let parcela of data) {
					for (let itemfaturamento of listaitensfaturamento) {
						if (parcela.id == itemfaturamento.id) {
							parcela.selecionado = true;
						}
					}
				}
			}
			
			$ctrl.calcularvalortotalparcelas();
			$ctrl.calcularvalorrestante();
			$ctrl.calcularhorasrestantesparcela();
		}
	});
	
	ParcelaService.buscartotalhoras(demanda.id, function (data){
		$ctrl.total_horas = data.total_horas;
	});
	
	ParcelaService.buscartotalhorasporvalorhora(demanda.id, function(data){
		
		$ctrl.objeto_horas_raw = {};
		
		for (let o of data) {
			
			if (!$ctrl.objeto_horas_raw[o.orcamentofase__id]) {
				$ctrl.objeto_horas_raw[o.orcamentofase__id] = {
					fase_id: o.orcamentofase__id,
					fase_descricao: o.orcamentofase__fase__descricao
				}
			}
			
			if (!$ctrl.objeto_horas_raw[o.orcamentofase__id][o.orcamentofase__itemfase__valor_hora__id]){
				$ctrl.objeto_horas_raw[o.orcamentofase__id][o.orcamentofase__itemfase__valor_hora__id] = {
					valor_hora_id: o.orcamentofase__itemfase__valor_hora__id,
					valor_hora_descricao: o.orcamentofase__itemfase__valor_hora__descricao,
					total_horas: o.total_horas,
					horas_restantes: o.total_horas
				}
			}
			
		}
		
		console.log($ctrl.objeto_horas_raw);
		
		$ctrl.calcularhorasrestantesparcela();
	});
	
	$ctrl.changetipoparcela = function () {
		$ctrl.parcelas = [];
	}
	
	$ctrl.calcularhorasrestantesparcela = function () {
		$ctrl.objeto_horas = {};
		angular.copy($ctrl.objeto_horas_raw, $ctrl.objeto_horas);
		if ($ctrl.parcelas){
			for (var i = 0; i < $ctrl.parcelas.length; i++) {
				var parcela = $ctrl.parcelas[i];
				if (!parcela.remover && parcela.parcelafases) {
					for (var pf = 0; pf < parcela.parcelafases.length; pf++) {
						var parcelafase = parcela.parcelafases[pf];
						if (!parcelafase.remover && parcelafase.medicoes){
							for (var m = 0; m < parcelafase.medicoes.length; m++){
								var medicao = parcelafase.medicoes[m];
								if (parcelafase.fase && medicao.valor_hora && medicao.quantidade_horas){
									$ctrl.objeto_horas[parcelafase.fase.id][medicao.valor_hora.id].horas_restantes-=medicao.quantidade_horas;
								}
							}
						}
					}
				}
			}
		}
	}
	
	$ctrl.calcularvalorrestante = function () {
		
		var valortotal = 0;
		for (var i in $ctrl.parcelas){
			var parcela = $ctrl.parcelas[i];
			if (!parcela.remover && parcela.valor_parcela){
				valortotal += CommonsService.stringparafloat(parcela.valor_parcela);
			}
		}
		
		var valor_restante = CommonsService.stringparafloat($ctrl.total_orcamento) - valortotal;
		$ctrl.valor_restante = CommonsService.formatarnumero(valor_restante);
	}
	
	$ctrl.remover = function (i, callback){
		i.remover = true;		
		if (callback){
			callback();
		}
	}
	
	var buscarquantidadefase = function (fase, valorhora) {
		var itensfase = fase.itensfase;
		if (itensfase) {
			for (var int = 0; int < itensfase.length; int++) {
				var itemfase = itensfase[int];
				if (itemfase.valor_hora.id == valorhora.id) {
					return itemfase.quantidade_horas;
				}
			}
		}
	}
	
	$ctrl.gerarparcelas = function (){
		
		$ctrl.parcelas = [];
		
		var currentDate = new Date();
		
		if (demanda.orcamento.total_orcamento && $ctrl.numero_vezes){
			var valorparcela = parseFloat(CommonsService.arredondar(CommonsService.stringparafloat(demanda.orcamento.total_orcamento) / $ctrl.numero_vezes));
			
			var valortotal = 0;
			
			for (var int = 0; int < $ctrl.numero_vezes; int++) {
				
				var parcela = {
					descricao: (int + 1) + '/' + $ctrl.numero_vezes,
					status: 'PE',
					parcelafases: [],
					data_previsto_parcela: CommonsService.dataparastring(currentDate)
				}
				
				currentDate.setMonth(currentDate.getMonth() + 1);
				
				$ctrl.parcelas.push(parcela);
				
				var total_fases = $ctrl.listafases.length;
				
				for (var lf = 0; lf < total_fases; lf++) {
					
					var fase = $ctrl.listafases[lf];
					
					var medicoes = [];
					
					for (let itemfase of fase.itensfase) {
						var valor_medicao = parseFloat(CommonsService.arredondar(CommonsService.stringparafloat(itemfase.valor_total) / $ctrl.numero_vezes));
						var horas = CommonsService.arredondar(valor_medicao * itemfase.quantidade_horas / CommonsService.stringparafloat(itemfase.valor_total));
						var medicao = {
							valor_hora: {
								id: itemfase.valor_hora.id
							},
							valor_total: CommonsService.formatarnumero(valor_medicao),
							quantidade_horas: horas							
						};
						medicoes.push(medicao);
						valortotal+=valor_medicao;
					}

					var parcelafase = {
						fase: fase,
						medicoes: medicoes
					}
					
					parcela.parcelafases.push(parcelafase);
					
				}
				
					
			}
			
			var ultimaparcela = $ctrl.parcelas[$ctrl.parcelas.length-1];
			
			var parcelafase = ultimaparcela.parcelafases[ultimaparcela.parcelafases.length - 1];
			
			var diferenca = parseFloat(CommonsService.arredondar(CommonsService.stringparafloat(demanda.orcamento.total_orcamento) - valortotal));
			diferenca = CommonsService.stringparafloat(parcelafase.medicoes[parcelafase.medicoes.length - 1].valor_total) + diferenca;
			
			parcelafase.medicoes[parcelafase.medicoes.length - 1].valor_total = CommonsService.formatarnumero(diferenca);
			
			var horas = CommonsService.arredondar(CommonsService.stringparafloat(parcelafase.medicoes[parcelafase.medicoes.length - 1].valor_total) * parcelafase.fase.itensfase[parcelafase.fase.itensfase.length - 1].quantidade_horas / CommonsService.stringparafloat(parcelafase.fase.itensfase[parcelafase.fase.itensfase.length - 1].valor_total));
			parcelafase.medicoes[parcelafase.medicoes.length - 1].quantidade_horas = horas;
			
			$ctrl.calcularvalortotalparcelas();
			$ctrl.calcularvalorrestante();
			
		}
		
	}
	
	$ctrl.calcularnumerohorasparcelas = function () {
		if ($ctrl.parcelas){
			for (var i = 0; i < $ctrl.parcelas.length; i++) {
				var parcela = $ctrl.parcelas[i];
				var numero_horas = (CommonsService.stringparafloat(parcela.valor_parcela) * $ctrl.total_horas) / CommonsService.stringparafloat($ctrl.total_orcamento);
				parcela.numero_horas = numero_horas;
			}
		}
	}
	
	$ctrl.gravarparcelas = function () {
		
		for (let parcela of $ctrl.parcelas) {
			if (parcela.descricao && parcela.data_previsto_parcela) {
				for (let parcelafase of parcela.parcelafases) {
					if (parcelafase.fase && parcelafase.fase.id) {
						for (let medicao of parcelafase.medicoes) {
							if (medicao.valor_hora && medicao.valor_hora.id && medicao.quantidade_horas && medicao.valor_total) {
								
							} else {
								medicao.remover = true;
							}
						}
					} else {
						parcelafase.remover = true;
					}
				}
			} else {
				parcela.remover = true;
			}
		}
		
		var objeto = {
			tipo_parcela: $ctrl.tipo,
			parcelas: $ctrl.parcelas,
			demanda_id: demanda.id
		}
		
		ParcelaService.gravarparcelas(objeto, function (data){
			ParcelaService.buscarparcelageradas(demanda.id, function (data){
				if (data) {
					$ctrl.parcelas = data;
					configurarparcelas($ctrl.parcelas);
					$ctrl.calcularvalortotalparcelas();
					$ctrl.calcularvalorrestante();
					$ctrl.calcularhorasrestantesparcela();
				} else {
					$ctrl.parcelas = [];
				}
				$window.alert('Parcelas geradas com sucesso!');	
			});
		});
	}
	
	$ctrl.adicionarparcela = function () {
		if (!$ctrl.parcelas){
			$ctrl.parcelas = [];
		}
		
		var parcelasfases = [];
		
		for (let fase of $ctrl.listafases) {
			
			var medicoes = [];
			
			for (var j = 0; j < fase.itensfase.length; j++) {
				medicoes.push({});			
			}
			
			parcelasfases.push({
				medicoes: medicoes
			});			
		}
		
		$ctrl.parcelas.push({
			status: 'PE',
			parcelafases: parcelasfases
		});
	}
	
	$ctrl.adicionarmedicao = function (parcelafase) {
		if (!parcelafase.medicoes) {
			parcelafase.medicoes = [];
		}
		
		parcelafase.medicoes.push({});
	}
	
	$ctrl.adicionarfase = function(parcela) {
		if (!parcela.parcelafases) {
			parcela.parcelafases = []
		}
		
		parcela.parcelafases.push({
			medicoes: [{}]
		});
		
	}
	
	$ctrl.removermedicao = function (medicao, parcelafase) {
		parcelafase.medicoes.splice(parcela.medicoes.indexOf(medicao), 1);
		$ctrl.calcularhorasrestantesparcela();
	}
	
	$ctrl.calcularvalortotalparcelas = function () {
		
		for (var p = 0; p < $ctrl.parcelas.length; p++) {
			var parcela = $ctrl.parcelas[p];
			var valortotalparcela = 0;
			if (parcela.parcelafases){
				for (var pf = 0; pf < parcela.parcelafases.length; pf++) {
					var parcelafase = parcela.parcelafases[pf];
					if(!parcelafase.remover){
						if (parcelafase.medicoes && parcelafase.medicoes.length > 0){
							for (var m = 0; m < parcelafase.medicoes.length; m++) {
								var medicao = parcelafase.medicoes[m];
								if (medicao.valor_total && !medicao.remover){
									valortotalparcela+=CommonsService.stringparafloat(medicao.valor_total);
								}
							}
						}
					}
				}
			}
			parcela.valor_parcela = CommonsService.formatarnumero(valortotalparcela);
		}
		
		$ctrl.verificarduplicidadefase = function (parcela, parcelafase, old_value) {
			
			for (let pf of parcela.parcelafases){
				if (pf != parcelafase && pf.fase && pf.fase.id == parcelafase.fase.id ) {
					alert("Este fase já está relacionado com esta parcela, favor selecionar outra");
					if (old_value) {
						parcelafase.fase.id = old_value;
					} else {
						parcelafase.fase.id = '';
					}
				}
			}
			
		}
		
		$ctrl.verificarduplicidade = function (parcelafase, medicao, old_value) {
			
			if (medicao.valor_hora.id && medicao.valor_hora.id != ''){
				for (let med of parcelafase.medicoes) {
					if (med != medicao && med.valor_hora && med.valor_hora.id == medicao.valor_hora.id) {
						alert("Este valor hora já está relacionado com esta fase, favor selecionar outro");
						if (old_value) {
							medicao.valor_hora.id = old_value;
						} else {
							medicao.valor_hora.id = '';
						}
					}
				}
			}
		}
		
		$ctrl.verificarduplicidadefase = function (parcelafase, old_value) {
			
		}
		
		$ctrl.calcularhorasmedicoes = function () {
			for (let parcela of $ctrl.parcelas) {
				var valortotalparcela = 0;
				if (parcela.parcelafases){
					for (var pf = 0; pf < parcela.parcelafases.length; pf++) {
						var parcelafase = parcela.parcelafases[pf];
						if(!parcelafase.remover){
							if (parcelafase.medicoes && parcelafase.medicoes.length > 0) {
								for (let medicao of parcelafase.medicoes) {
									if (medicao.valor_hora && medicao.valor_total){
										var fase;
	
										for (let f of $ctrl.listafases) {
											if (f.id == parcelafase.fase.id){
												fase = f;
												break;
											}
										}
										
										var itemfase;
										
										for (let item of fase.itensfase) {
											if (item.valor_hora.id == medicao.valor_hora.id) {
												itemfase = item;
												break;
											}
										}
										
										var horas = CommonsService.arredondar(CommonsService.stringparafloat(medicao.valor_total) * itemfase.quantidade_horas / CommonsService.stringparafloat(itemfase.valor_total));
										medicao.quantidade_horas = horas;
									}
								}
							}
						}
					}
				}
				
			}
			
			$ctrl.calcularvalortotalparcelas();
			$ctrl.calcularvalorrestante();
			$ctrl.calcularhorasrestantesparcela();
			
		}
			
		
		$ctrl.calcularvalorrestante();
		$ctrl.calcularhorasrestantesparcela();
		
	}
	
	$ctrl.changevalorhora = function (medicao) {
		
		var valor_hora_id = medicao.valor_hora.id;
		$ctrl.calcularvalortotalparcelas();
		$ctrl.calcularhorasrestantesparcela();

	}
	
	$ctrl.changequantidadehoras = function(medicao){
		
		if (medicao.quantidade_horas && medicao.quantidade_horas.replace) {
			medicao.quantidade_horas = medicao.quantidade_horas.replace(/[^0-9\.]/g, '');
		}
		
		if (medicao.valor_hora){
			var valor_hora_id = medicao.valor_hora.id;
			var vigencia;
			
			for (var int = 0; int < $ctrl.listavalorhora.length; int++) {
				var valorhora = $ctrl.listavalorhora[int];
				if (valorhora.id == valor_hora_id) {
					vigencia = valorhora.vigencia;
					break;
				}
			}
		}
		
		if (medicao.valor_hora && vigencia){
			medicao.valor_total = CommonsService.formatarnumero(vigencia.valor * medicao.quantidade_horas);
		}
		
		$ctrl.calcularvalortotalparcelas();
		$ctrl.calcularvalorrestante();
		$ctrl.calcularhorasrestantesparcela();
		
	}
	
	$ctrl.selecionarparcelas = function () {
		let array = [];
		
		for (let parcela of $ctrl.parcelas) {
			if (parcela.selecionado) {
				array.push(parcela);
			}
		}
		
		$uibModalInstance.close(array);
		
	}
	
	$ctrl.fechar = function (){
		$uibModalInstance.close()	
	}
	
});
