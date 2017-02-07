"use strict";

demandas.controller('OrcamentoAtividadeController', function($rootScope, ValorHoraService, $uibModal, FaseService, CommonsService, share){
	var $ctrl = this;
	$ctrl.share = share;
	
	$ctrl.listavalorhorab2card = ValorHoraService.buscarvalorhorab2card();
	
	$rootScope.$on('atividades', function(event, data) {
		if (data.cliente){
			share.listavalorhora = ValorHoraService.buscarvalorhoraporcliente(data.cliente.id);
		}
		
		if (share.demanda.orcamento.orcamento_atividades &&
				share.demanda.orcamento.orcamento_atividades.length > 0) {
			
			$ctrl.colunas = [];
			var lista_colunas = [];
			for (let orcamento_atividade of share.demanda.orcamento.orcamento_atividades){
				
				for (var valor_hora_id in orcamento_atividade.colunas){
					if(lista_colunas.indexOf(valor_hora_id) < 0){
						lista_colunas.push(valor_hora_id)
						$ctrl.colunas.push({
							valor_hora: {
								id:parseInt(valor_hora_id)
							}
						});
					}
				}
				
			}
			
			$ctrl.calculartotaiscolunas();
			
		} else {
			$ctrl.colunas = [{},{}];
			share.demanda.orcamento.orcamento_atividades = [];
			for (var int = 0; int < 20; int++) {
				share.demanda.orcamento.orcamento_atividades.push({
					colunas : {}
				});
			}
		}
	});
	
	if ($ctrl.share.demanda.$promise) {
		$ctrl.share.demanda.$promise.then(function (data) {
			$rootScope.$emit('atividades', data);
		});
	} else {
		$ctrl.colunas = [{}, {}];
		share.demanda.orcamento.orcamento_atividades = [];
		for (var int = 0; int < 20; int++) {
			share.demanda.orcamento.orcamento_atividades.push({
				colunas : {}
			});
		}
	}
	
	$ctrl.calculartotaiscolunas = function () {
		if ($ctrl.share.demanda.orcamento.orcamento_atividades) {
			var total_colunas = 0; 
			for (let coluna of $ctrl.colunas) {
				coluna.valor_total = 0;
				for (let orcamento_atividade of $ctrl.share.demanda.orcamento.orcamento_atividades){
					if (!orcamento_atividade.remover){
						for (var valor_hora_id in orcamento_atividade.colunas){
							if (coluna.valor_hora && coluna.valor_hora.id == valor_hora_id){
								coluna.valor_total+=orcamento_atividade.colunas[valor_hora_id].horas;
								total_colunas+=orcamento_atividade.colunas[valor_hora_id].horas;
							}
						}
					}
				}
			}
			$ctrl.total_colunas = total_colunas;
		}
	}
	
	$ctrl.remover = function (i, callback){
		i.remover = true;		
		if (callback){
			callback();
		}
	}
	
	$ctrl.removercoluna = function (coluna){
		
		for (let orcamento_atividade of $ctrl.share.demanda.orcamento.orcamento_atividades){
			if (orcamento_atividade.colunas && coluna.valor_hora && coluna.valor_hora.id ){
				delete orcamento_atividade.colunas[coluna.valor_hora.id]
			}
		}
		
		$ctrl.colunas.splice($ctrl.colunas.indexOf(coluna), 1);
		
		$ctrl.changecoluna();	
		$ctrl.calculartotaiscolunas();
		
	}
	
	$ctrl.adicionarcoluna = function () {
		$ctrl.colunas.push({});
	}
	
	$ctrl.validarcolunaalterada = function (coluna, valorhora_old) {
		
		if (coluna.valor_hora.id){
			
			var repetido = false;
			
			for (let c of $ctrl.colunas) {
				if (c.valor_hora){
					if (c != coluna && c.valor_hora.id == coluna.valor_hora.id) {
						repetido = true;
						break;
					}
				}
			}
			
			if (!repetido){
				if ($ctrl.share.demanda.orcamento.orcamento_atividades) {
					for (let orcamento_atividade of $ctrl.share.demanda.orcamento.orcamento_atividades) {
						if (orcamento_atividade.colunas && coluna.valor_hora && coluna.valor_hora.id ){
							delete orcamento_atividade.colunas[coluna.valor_hora.id];
						}
					}
				}
				
				$ctrl.changecoluna();	
				$ctrl.calculartotaiscolunas();
				
			} else {
				coluna.valor_hora.id = valorhora_old;
				alert('Valor de coluna repetido.');
			}
		}
	}
	
	$ctrl.adicionaratividade = function () {
		if (!$ctrl.share.demanda.orcamento.orcamento_atividades) {
			$ctrl.share.demanda.orcamento.orcamento_atividades = [];
		}
		
		var atividade = {
			colunas : {}
		}
		
		$ctrl.share.demanda.orcamento.orcamento_atividades.push({});
		
	}
	
	$ctrl.changecoluna = function(){
		
		var total = 0;
		if ($ctrl.share.demanda.orcamento.orcamento_atividades){
			for (let orcamento_atividade of $ctrl.share.demanda.orcamento.orcamento_atividades){
				var total = 0;
				for (let coluna of $ctrl.colunas) {
					if (coluna.valor_hora && orcamento_atividade.colunas && orcamento_atividade.colunas[coluna.valor_hora.id]) {
						total+=orcamento_atividade.colunas[coluna.valor_hora.id].horas;
					}
				}
				orcamento_atividade.total_horas = total;
			}
		}
		
		$ctrl.calculartotaiscolunas();
		
	}
	
});