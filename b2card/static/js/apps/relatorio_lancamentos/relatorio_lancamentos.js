"use strict";

var relatorio_lancamentos = angular.module('relatorio_lancamentos', ['relatorio_lancamentos-services', 'pessoa-services', 'demandas-services', 'inicial-services', 'tipoalocacao-services', 'commons', 'ui.bootstrap', 'ui.mask', 'ngMaterial']);

relatorio_lancamentos.controller('RelatorioLancamentosController', function (RelatorioLancamentosService, PessoaService, DemandaService, CommonsService, $scope, $window, $uibModal){
	var $ctrl = this;
	$ctrl.show = true;
	
	$ctrl.modaldata = {}
	
	$ctrl.listaclientes= PessoaService.buscarpessoasjuridicas();
	$ctrl.listafuncionarios = PessoaService.buscarprofissionais();
	
	RelatorioLancamentosService.ehgestor(function (data){
		$ctrl.eh_gestor = data.gestor;
	});
	
	$ctrl.datepicker_options = {
		datepickerMode: 'month',
		minMode: 'month'
	}

	$ctrl.abrirmodalalocacao = (alocacao) => {
		
		RelatorioLancamentosService.verificartipodemanda(alocacao.id, function(data){
			
			if (data.tipo_demanda == 'E'){

				var modalInstance = $uibModal.open({
					animation : $ctrl.animationsEnabled,
					ariaLabelledBy : 'modal-title',
					ariaDescribedBy : 'modal-body',
					templateUrl : '/static/modal/modalAtualizarAlocacao.html?bust=' + Math.random().toString(36).slice(2),
					controller : 'ModalAlocacaoController',
					controllerAs : '$ctrl',
					//size : 'lg'
					windowClass: 'app-modal-window',
					resolve : {
				    	  alocacao: alocacao
					}
				});
					
				modalInstance.result.then(function(data) {
					$ctrl.pesquisar();
				}, function() {
					// $log.info('Modal dismissed at: ' + new Date());
				});
				
			} else {
				var modalInstance = $uibModal.open({
					animation : $ctrl.animationsEnabled,
					ariaLabelledBy : 'modal-title',
					ariaDescribedBy : 'modal-body',
					templateUrl : '/static/modal/modalAtualizarAlocacaoInterna.html?bust=' + Math.random().toString(36).slice(2),
					controller : 'ModalAlocacaoInternaController',
					controllerAs : '$ctrl',
					//size : 'lg'
					windowClass: 'app-modal-window',
					resolve : {
						alocacao: alocacao
					}
				});
					
				modalInstance.result.then(function(data) {
					$ctrl.pesquisar();
				}, function() {
					// $log.info('Modal dismissed at: ' + new Date());
				});
			}
			
		});
		
	}
	
	$ctrl.listademandas = [];
	
	$ctrl.abrirmodaldata = prop => {
		$ctrl.modaldata[prop] = !$ctrl.modaldata[prop] 
	}
	
	$ctrl.buscardemandas = (texto) => {
		DemandaService.buscardemandaportexto(texto, function (data) {
			
			for(let demanda of data) {
				demanda.nome_demanda = CommonsService.pad(demanda.id, 5) + ' - ' + demanda.nome_demanda;
			}
			
			$ctrl.listademandas = data;
		});	
	}
	
	$ctrl.listaalocacao = [];
	
	$ctrl.total_horas = 0;
	
	$ctrl.pesquisar = () => {
		RelatorioLancamentosService.pesquisar($ctrl.arguments, function (data){
			$ctrl.listaalocacao = data;
			let total_horas_milisegundos = 0;
			for(let alocacao of data) {
				alocacao.horas_alocadas = CommonsService.milliparahoras(alocacao.horas_alocadas_milisegundos);
				total_horas_milisegundos+=alocacao.horas_alocadas_milisegundos;
			}
			
			$ctrl.total_horas = CommonsService.milliparahoras(total_horas_milisegundos);
			
		});
	}
	
}).controller('ModalAlocacaoInternaController', function (alocacao, RelatorioLancamentosService, CommonsService, TipoAlocacaoService, $uibModalInstance, $scope, $window) {
	
	var $ctrl = this;
	$ctrl.atividade = alocacao.atividade_profissional.atividade;
	
	$ctrl.data = CommonsService.stringparadata(alocacao.data_informada);
	$ctrl.hora_inicio = alocacao.hora_inicio;
	$ctrl.hora_fim = alocacao.hora_fim;
	
	$scope.today = function() {
		$ctrl.data =new Date();
	};
	
	$scope.clear = function() {
		$scope.dt = null;
	};

	$ctrl.abrir = function() {
		$ctrl.aberto = true;
	};
	
	$ctrl.cancelar= function (){
		$uibModalInstance.close();
	}
	
	$ctrl.excluir = () => {
		if (confirm(MESSAGE_EXCLUIR)) {
			RelatorioLancamentosService.excluiralocacaointerna(alocacao.id, function (result) {
				$uibModalInstance.close(result);
			});
		}
	}
	
	$ctrl.salvar = () => {
		
		if (!$ctrl.data) {
			alert('Informe data.')
			return;
		}
		
		if (!$ctrl.hora_inicio){
			alert('Informe hora inicio.');
			return;
		}
		
		if(!$ctrl.hora_fim) {
			alert('Informe hora fim.');
			return;
		}
		
		var hora_inicio = $ctrl.hora_inicio.split(':');
		var hora_fim = $ctrl.hora_fim.split(':');
		
		hora_inicio = new Date(0, 0, 0, hora_inicio[0], hora_inicio[1], 0, 0);
		hora_fim = new Date(0,0,0,hora_fim[0], hora_fim[1], 0,0).getTime();
		
		if (hora_inicio >= hora_fim) {
			alert('Hora inicio deve ser menor que hora fim.');
			return;
		}
		
		var milisegundos = hora_fim - hora_inicio
		
		if ($ctrl.data instanceof Date){
			$ctrl.data = CommonsService.dataparastring($ctrl.data);
		}
	
		var data = {
			alocacao_id: alocacao.id,
			horas_alocadas_milisegundos : milisegundos,
			hora_inicio: $ctrl.hora_inicio,
			hora_fim: $ctrl.hora_fim,
			data_informada: $ctrl.data,
		}	

		RelatorioLancamentosService.salvaralocacaointerna(data, function (data) {
			$uibModalInstance.close(data);
		});
		
	}
	
}).controller('ModalAlocacaoController', function (alocacao, CommonsService, InicialService, RelatorioLancamentosService, TipoAlocacaoService, $uibModalInstance, $scope, $window) {
	var $ctrl = this;
	$ctrl.atividade = alocacao.atividade_profissional.atividade;
	$ctrl.atividade_fechada;
	
	InicialService.buscarultimaalocacao(alocacao.atividade_profissional.id, function (data){
		$ctrl.percentual_conclusao = data.percentual_concluido;
		if (data.percentual_concluido == 100){
			$ctrl.atividade_fechada = true;
		}
	});
	
	$ctrl.tipoalocacaolist = TipoAlocacaoService.buscartipoalocacoes();
	
	$ctrl.data = CommonsService.stringparadata(alocacao.data_informada);
	$ctrl.hora_inicio = alocacao.hora_inicio;
	$ctrl.hora_fim = alocacao.hora_fim;
	$ctrl.percentual_conclusao = alocacao.percentual_concluido;
	$ctrl.tipo_alocacao = alocacao.tipo_alocacao;
	
	$scope.today = function() {
		$ctrl.data =new Date();
	};

	$scope.clear = function() {
		$scope.dt = null;
	};

	$ctrl.abrir = function() {
		$ctrl.aberto = true;
	};
	
	$ctrl.cancelar= function (){
		$uibModalInstance.close();
	}
	
	$ctrl.excluir = () => {
		if (confirm(MESSAGE_EXCLUIR)) {
			RelatorioLancamentosService.excluiralocacao(alocacao.id, function (result) {
				$uibModalInstance.close(result);
			});
		}
	}
	
	$ctrl.salvar = () => {
		
		let data = CommonsService.dataparaurl($ctrl.data);
		
		RelatorioLancamentosService.validardatahora (alocacao.id, $ctrl.atividade.id, data, $ctrl.hora_inicio, $ctrl.hora_fim, function(result) {
			
			if(result.custo_prestador && !result.possui_alocacao) {
			
				if (!$ctrl.data) {
					alert('Informe data.')
					return;
				}
				
				if (!$ctrl.percentual_conclusao) {
					alert('Informe % conclusão.');
					return;
				}
				
				if (!$ctrl.hora_inicio){
					alert('Informe hora inicio.');
					return;
				}
				
				if(!$ctrl.hora_fim) {
					alert('Informe hora fim.');
					return;
				}
				
				if($ctrl.atividade_fechada && (!$ctrl.tipo_alocacao || !$ctrl.tipo_alocacao.id)) {
					alert('Informe tipo de alocação.');
					return;
				}
				
				var hora_inicio = $ctrl.hora_inicio.split(':');
				var hora_fim = $ctrl.hora_fim.split(':');
				
				hora_inicio = new Date(0, 0, 0, hora_inicio[0], hora_inicio[1], 0, 0);
				hora_fim = new Date(0,0,0,hora_fim[0], hora_fim[1], 0,0).getTime();
				
				if (hora_inicio >= hora_fim) {
					alert('Hora inicio deve ser menor que hora fim.');
					return;
				}
				
				var milisegundos = hora_fim - hora_inicio
	
				if ($ctrl.data instanceof Date){
					$ctrl.data = CommonsService.dataparastring($ctrl.data);
				}
				
				var data = {
					alocacao_id: alocacao.id,
					horas_alocadas_milisegundos : milisegundos,
					percentual_concluido : $ctrl.percentual_conclusao,
					hora_inicio: $ctrl.hora_inicio,
					hora_fim: $ctrl.hora_fim,
					data_informada: $ctrl.data,
					observacao: $ctrl.observacao,
					tipo_alocacao: $ctrl.tipo_alocacao
				}
				
				RelatorioLancamentosService.salvaralocacao(data, function (data) {
					$uibModalInstance.close(data);
				});
			
			} else {
				alert('Você não possui vigência para esta data, favor verificar!');
			}
			
		});
		
	}
	
});