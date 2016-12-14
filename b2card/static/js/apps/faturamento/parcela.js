"use strict";

demandas.controller('ModalParcelasController', function ($scope, $window, $uibModalInstance, demanda, listavalorhora, CommonsService, ParcelaService){
	var $ctrl = this;
	
	$ctrl.demanda = demanda;
	$ctrl.total_orcamento = demanda.orcamento.total_orcamento;
	$ctrl.listavalorhora = listavalorhora;
	$ctrl.listafases = demanda.orcamento.fases;
	
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
							if (medicao.valor){
								medicao.valor = CommonsService.formatarnumero(medicao.valor);
							}
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
			$ctrl.calcularvalortotalparcelas();
			$ctrl.calcularvalorrestante();
			$ctrl.calcularhorasrestantesparcela();
		}
	});
	
	ParcelaService.buscartotalhoras(demanda.id, function (data){
		$ctrl.total_horas = data.total_horas;
	});
	
	ParcelaService.buscartotalhorasporvalorhora(demanda.id, function(data){
		$ctrl.valorhoras_horas_raw = data;
		
		for (var i = 0; i < $ctrl.valorhoras_horas_raw.length; i++){
			$ctrl.valorhoras_horas_raw[i].horas_restantes = $ctrl.valorhoras_horas_raw[i].total_horas;
		}
		
		$ctrl.calcularhorasrestantesparcela();
	});
	
	$ctrl.changetipoparcela = function () {
		$ctrl.parcelas = [];
	}
	
	$ctrl.calcularhorasrestantesparcela = function () {
		$ctrl.valorhoras_horas = [];
		angular.copy($ctrl.valorhoras_horas_raw, $ctrl.valorhoras_horas);
		if ($ctrl.parcelas){
			for (var i = 0; i < $ctrl.parcelas.length; i++) {
				var parcela = $ctrl.parcelas[i];
				if (!parcela.remover && parcela.parcelafases) {
					for (var pf = 0; pf < parcela.parcelafases.length; pf++) {
						var parcelafase = parcela.parcelafases[pf];
						if (!parcelafase.remover && parcelafase.medicoes){
							for (var m = 0; m < parcelafase.medicoes.length; m++){
								var medicao = parcelafase.medicoes[m];
								for (var j = 0; j < $ctrl.valorhoras_horas.length; j++){
									var valorhora_hora = $ctrl.valorhoras_horas[j];
									if (!medicao.remover && medicao.quantidade_horas && medicao.valor_hora.id == valorhora_hora.fase__itemfase__valor_hora__id){
										valorhora_hora.horas_restantes -= medicao.quantidade_horas;
									}
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
	
	var calcularvalormedicoes = function () {
		for (let parcela of $ctrl.parcelas) {
			for (let parcelafase of parcela.parcelafases) {
				for (let medicao of parcelafase.medicoes) {
					if (medicao.valor){
						medicao.valor_total = CommonsService.formatarnumero(CommonsService.stringparafloat(medicao.valor) * medicao.quantidade_horas);
					} 
				}
			}
		}
	}
	
	$ctrl.gerarparcelas = function (){
		
		$ctrl.parcelas = [];
		
		if (demanda.orcamento.total_orcamento && $ctrl.numero_vezes){
			var valorparcela = parseFloat(CommonsService.arredondar(CommonsService.stringparafloat(demanda.orcamento.total_orcamento) / $ctrl.numero_vezes));
			
			var valortotal = 0;
			
			for (var int = 0; int < $ctrl.numero_vezes; int++) {
				
				var parcela = {
					descricao: (int + 1) + '/' + $ctrl.numero_vezes,
					status: 'PE',
					parcelafases: []
				}
				
				$ctrl.parcelas.push(parcela);
				
				var total_fases = $ctrl.listafases.length;
				
				for (var lf = 0; lf < total_fases; lf++) {
					
					var fase = $ctrl.listafases[lf];
					var valorparcelafase = parseFloat(CommonsService.arredondar(valorparcela / total_fases));
					
					var parcelafase = {
						fase: fase,
						valor: CommonsService.formatarnumero(valorparcelafase)
					}
					
					valortotal+=valorparcelafase;
					parcela.parcelafases.push(parcelafase);
					
				}
				
					
			}
			
			var ultimaparcela = $ctrl.parcelas[$ctrl.parcelas.length-1];
			
			var diferenca = CommonsService.stringparafloat(demanda.orcamento.total_orcamento) - valortotal;
			diferenca = CommonsService.stringparafloat(ultimaparcela.parcelafases[ultimaparcela.parcelafases.length - 1].valor) + diferenca;
			
			ultimaparcela.parcelafases[ultimaparcela.parcelafases.length - 1].valor = CommonsService.formatarnumero(diferenca);
			
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
		$ctrl.parcelas.push({
			status: 'PE',
			parcelafases: [{
				medicoes: [{}]
			}]
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
						} else if (parcelafase.valor) {
							valortotalparcela+=CommonsService.stringparafloat(parcelafase.valor);
						}
					}
				}
			}
			parcela.valor_parcela = CommonsService.formatarnumero(valortotalparcela);
			
		}
		
		$ctrl.calcularvalorrestante();
		$ctrl.calcularhorasrestantesparcela();
		
	}
	
	$ctrl.changevalorhora = function (medicao) {
		
		var valor_hora_id = medicao.valor_hora.id;
		
		for (var int = 0; int < $ctrl.listavalorhora.length; int++) {
			var valorhora = $ctrl.listavalorhora[int];
			if (valorhora.id == valor_hora_id) {
				medicao.valor =  CommonsService.formatarnumero(valorhora.vigencia.valor);
				break;
			}
		}
		
		$ctrl.calcularvalortotalparcelas();
		$ctrl.calcularhorasrestantesparcela();

	}
	
	$ctrl.changequantidadehoras = function(medicao){
		if (medicao.valor){
			medicao.valor_total = CommonsService.formatarnumero(CommonsService.stringparafloat(medicao.valor) * medicao.quantidade_horas);
		}
		
		$ctrl.calcularvalortotalparcelas();
		$ctrl.calcularvalorrestante();
		$ctrl.calcularhorasrestantesparcela();
		
	}
	
	$ctrl.fechar = function (){
		$uibModalInstance.close()	
	}
	
});
