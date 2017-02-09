"use strict";

var demandas = angular.module('demandas', ['demandas-services', 'pessoa-services', 'centrocusto-services', 'naturezademanda-services', 'fase-services', 'valorhora-services', 'parcela', 'parcela-services',
                                           'centroresultado-services', 'unidadeadministrativa-services', 'ui.bootstrap', 'commons', 'ui.mask',  'ngMaterial']);

demandas.config(['$httpProvider', 'CommonsServiceProvider', function($httpProvider, CommonsServiceProvider) {  
    $httpProvider.interceptors.push(function () {
    	return {
    		response: function (config, CommonsService) {
	        	var ajustardados = demanda => {
	        		if(demanda){
	        			CommonsService = CommonsServiceProvider.$get()
	        			if (demanda.data_criacao) {
	        				demanda.data_criacao = CommonsService.stringparadata(demanda.data_criacao);
	        			}
		        		if (demanda.fase_atividades){
		        			for(let fase_atividade of demanda.fase_atividades){
		        				if (fase_atividade.atividades){
		        					for (let atividade of fase_atividade.atividades){
		        						atividade.data_inicio_string = atividade.data_inicio;
		        						atividade.data_fim_string = atividade.data_fim;
		        						
		        						atividade.data_inicio = CommonsService.stringparadata(atividade.data_inicio);
		        						atividade.data_fim = CommonsService.stringparadata(atividade.data_fim);
		        					}
		        				}
		        			}
		        		}
		        		
		        		if (demanda.orcamento) {
		        			demanda.orcamento.total_despesas = CommonsService.formatarnumero(demanda.orcamento.total_despesas);
		        			if (demanda.orcamento.despesas) {
		        				for (let despesa of demanda.orcamento.despesas) {
		        					despesa.valor = CommonsService.formatarnumero(despesa.valor);
		        				}
		        			}
		        		}
		        		
	        		}
	        	}
	        	ajustardados(config.data);
	        	return config;
	        }
    	}
    });
}]);

demandas.factory('share', function(){
	  return {};
});

demandas.controller('DemandaController', function ($rootScope, $scope, $window, $uibModal, $log, DemandaService, ParcelaService, PessoaService,
		CentroCustoService, ValorHoraService, CommonsService, AutenticationService, CentroResultadoService, UnidadeAdministrativaService, NaturezaDemandaService, share, MessageService){
	var $ctrl = this; 
	
	var messageinfo = function (msg){
		$ctrl.clazz = 'label-primary';	
		$ctrl.message = msg;
	}

	var messagesuccess = function (msg) {
		$ctrl.clazz = 'label-success';
		$ctrl.message = msg;
	}
	
	$ctrl.layout = function (i){
		if (i.show) {
			i.show = !i.show;
		} else {
			i.show = true;
		}
	};
	
	$ctrl.changecliente = function () {
		if ($ctrl.demanda.cliente){
			share.listavalorhora = ValorHoraService.buscarvalorhoraporcliente($ctrl.demanda.cliente.id);
		}
	}
	
	var configurardemanda = function (demanda_id) {
	
		if (demanda_id) {
			$ctrl.demanda = DemandaService.buscardemanda(demanda_id, function (data){
				
				$ctrl.show=true;
				
				var ocorrencias = data.ocorrencias;
				for ( var i in ocorrencias ){
					ocorrencias[i].show = false;
				}
				
				var tarefas = data.tarefas;
				for ( var i in tarefas ){
					tarefas[i].show = false;
				}
				
				if (data.cliente.id) {
					share.listavalorhora = ValorHoraService.buscarvalorhoraporcliente(data.cliente.id);
					if (share.listavalorhora.$promise) {
						share.listavalorhora.$promise.then(function (data) {
							$rootScope.$emit('calculardesejado');
							$rootScope.$emit('calcularprojetado');
							$rootScope.$emit('calcularproposto');
							$rootScope.$emit('incluirfasesorcamento');
						});
					}
				}
				
				$ctrl.listacentroresultadoshoras = DemandaService.buscarcentroresultadoshora(demanda_id);
				
			});
			
			share.demanda = $ctrl.demanda;
			
		} else {
			$ctrl.demanda = {
				'propostas':[{}],
				'observacoes':[{}],
				'ocorrencias':[{}],
				'orcamento': {
					'margem_risco': 15,
					'lucro_desejado': 30,
					'total_despesas': '0,00',
					'imposto_devidos': 0
				},
				'fase_atividades':[],
				'data_criacao': new Date()
			}
			$ctrl.show=true;
			$ctrl.listacentroresultadoshoras = []
			share.demanda = $ctrl.demanda;
		}
	
	}
	
	$ctrl.abrirmodaldatademanda = () => {
		$ctrl.data_demanda = true;	
	}
	
	configurardemanda(demanda_id);
	
	$ctrl.adicionarproposta = function () {
		$ctrl.demanda.propostas.unshift({});
	}
	
	$ctrl.adicionarobservacao = function (){
		$ctrl.demanda.observacoes.unshift({})
	}
	
	$ctrl.adicionarocorrencia = function () {
		var ocorrencia = {'show': true};
		$ctrl.demanda.ocorrencias.unshift(ocorrencia);
	}
	
	$ctrl.remover = function (i, callback){
		i.remover = true;		
		if (callback){
			callback();
		}
	}
		
	$ctrl.listaclientes= PessoaService.buscarpessoasjuridicas();
	$ctrl.listafuncionarios = PessoaService.buscarprofissionais();
	$ctrl.listagestores = PessoaService.buscargestores();
	
	// TODO mudar isso depois... 
	share.listafuncionarios = $ctrl.listafuncionarios;
	
	$ctrl.listacentroresultados = CentroResultadoService.buscarcentroresultados();
	$ctrl.listaunidadeadministrativas = UnidadeAdministrativaService.buscarunidadeadministrativas();
	$ctrl.listanaturezademanda = NaturezaDemandaService.buscarnaturezademandas();
	
	var abas = ['#dadosdemanda', '#orcamento', '#atividades', 
		'#proposta', '#tarefas', '#observacoes', '#ocorrencias', '#resumo']
	
	$ctrl.listaabasautorizadas = AutenticationService.buscarabasautorizadas(abas);
	
	$ctrl.salvardemanda = function (){
		MessageService.clear();
		$ctrl.bloquearsalvar = true;
		share.demanda = DemandaService.salvardemanda($ctrl.demanda, function(data){
			$ctrl.demanda = data;
			
			$ctrl.listacentroresultadoshoras = DemandaService.buscarcentroresultadoshora(data.id);
			MessageService.messagesuccess('Salvo com sucesso!')
			$ctrl.bloquearsalvar = false;
		});
		
		if (share.demanda.$promise){
			share.demanda.$promise.then(function (data) {
				$rootScope.$emit('orcamento', data);
				$rootScope.$emit('atividades', data);
				$rootScope.$emit('calculardesejado');
				$rootScope.$emit('calcularprojetado');
				$rootScope.$emit('calcularproposto');
				$rootScope.$emit('incluirfasesorcamento');
			});
		}
	}
	
	$ctrl.deletar = function () {
		if(confirm(MESSAGE_EXCLUIR)) {
			DemandaService.deletardemanda($ctrl.demanda.id, function(data){
				$window.location.href = BASE_URL + 'demandas/';
			});
		}
	}
	
	$ctrl.verificardisponibilidadeaba = function(aba){
		if (!$ctrl.listaabasautorizadas || $ctrl.listaabasautorizadas.length == 0) {
			return true;
		}
		
		for (let i of $ctrl.listaabasautorizadas) {
			if (i == aba){
				return true;
			}
		}
		
		return false;
		
	}
	
}).controller('AtividadeController', function($rootScope, ValorHoraService, DemandaService, FaseService, CommonsService, PessoaService, share){
	var $ctrl = this;
	$ctrl.share = share;
	
	$ctrl.listafases = FaseService.buscarfases();
	//$ctrl.listagestores = PessoaService.buscargestores();
	var atividadeprofissional = {}
	
	$ctrl.remover = function (i, callback){
		i.remover = true;		
		if (callback){
			callback();
		}
	}
	
	$ctrl.removeratividade = function (i, callback){
		if (i.id) {
			DemandaService.verificarseatividadepossuialocacao(i.id, function (data){
				if (data.possui) {
					alert('Atividade não pode ser removida pois já possui apropriação.')
					return;
				} else {
					i.remover = true;		
					if (callback){
						callback();
					}		
				}
			});
		} else {
			i.remover = true;		
			if (callback){
				callback();
			}
		}
	}
	
	$ctrl.adicionarfase = function (){
		
		if (!$ctrl.share.demanda.fase_atividades){
			$ctrl.share.demanda.fase_atividades = [];
		}
		
		$ctrl.share.demanda.fase_atividades.push({});
		
	}
	
	$ctrl.listaresponsavelfase = [];
	$ctrl.buscarresponsavelfase = texto => {
		if (texto){
			PessoaService.buscarprofissional(texto, function (data){
				$ctrl.listaresponsavelfase=data;
			}); 
		}
	} 
	
	$ctrl.limparlistaresponsavelfase = function () {
		$ctrl.listaresponsavelfase = [];
	}
	
	$ctrl.atividadeprofissionalmap = {};
	$ctrl.atividadeprofissionallist = [];
	
	$ctrl.buscarprofissional = function (texto, atividadeprofissional){
		if (texto){
			PessoaService.buscarprofissional(texto, function (data){
				$ctrl.atividadeprofissionallist = data;
			}); 
		}
	}
	
	$ctrl.limparlistaatividadeprofissionallist = function () {
		$ctrl.atividadeprofissionallist = [];
	}
	
	$ctrl.adicionaratividade = function (fase_atividade) {
		if (!fase_atividade.atividades){
			fase_atividade.atividades = [];
		}
		
		var atividadeprofissional = {};
		fase_atividade.atividades.push({
			atividadeprofissionais: [atividadeprofissional]
		});	
		
	}

	$ctrl.alteracaodatafaseatividade = () => {
		
		var data_inicio_demanda;
		var data_fim_demanda;
		
		if ($ctrl.share.demanda.fase_atividades) {
			for (let fase_atividade of $ctrl.share.demanda.fase_atividades) {
				if (fase_atividade.data_inicio) {
					if (data_inicio_demanda) {
						let data_inicio = CommonsService.stringparadata(fase_atividade.data_inicio);
						if (data_inicio_demanda > data_inicio) {
							data_inicio_demanda = data_inicio;
						}
					} else {
						data_inicio_demanda = CommonsService.stringparadata(fase_atividade.data_inicio);
					}
				}
				
				if (fase_atividade.data_fim) {
					if (data_fim_demanda) {
						let data_fim = CommonsService.stringparadata(fase_atividade.data_fim);
						if (data_fim_demanda < data_fim){
							data_fim_demanda = data_fim;
						}
					} else {
						data_fim_demanda = CommonsService.stringparadata(fase_atividade.data_fim);
					}
				}
				
			}
		}
		
		if (data_inicio_demanda) {
			$ctrl.share.demanda.data_inicio = CommonsService.dataparastring(data_inicio_demanda);
		}
		
		if (data_fim_demanda){
			$ctrl.share.demanda.data_fim = CommonsService.dataparastring(data_fim_demanda)
		}
		
	}
	
	$ctrl.alteracaodataatividade = (fase_atividade, atividadeselecionada, propriedade, old_value) => {
		
		if (atividadeselecionada.data_inicio)
			var data_inicio_selecionada = CommonsService.stringparadata(atividadeselecionada.data_inicio);
		if (atividadeselecionada.data_fim)
			var data_fim_selecionada = CommonsService.stringparadata(atividadeselecionada.data_fim);
		
		if (data_inicio_selecionada && data_fim_selecionada && data_inicio_selecionada > data_fim_selecionada) {
			atividadeselecionada[propriedade] = old_value;
			alert('Verificar se as datas estão corretas');
			return;
		}
		
		var data_inicio_fase;
		var data_fim_fase;
		
		if (fase_atividade.atividades) {
			for(let atividade of fase_atividade.atividades) {
				if (atividade.data_inicio) {
					if (data_inicio_fase) {
						let data_inicio = CommonsService.stringparadata(atividade.data_inicio);
						if (data_inicio_fase > data_inicio) {
							data_inicio_fase = data_inicio;
						}
					} else {
						data_inicio_fase = CommonsService.stringparadata(atividade.data_inicio);
					}
				}
				if (atividade.data_fim) {
					if (data_fim_fase) {
						let data_fim = CommonsService.stringparadata(atividade.data_fim);
						if (data_fim_fase < data_fim) {
							data_fim_fase = data_fim;
						}
					} else {
						data_fim_fase = CommonsService.stringparadata(atividade.data_fim);
					}
				}
			}
		}
		
		if (data_inicio_fase) {
			fase_atividade.data_inicio = CommonsService.dataparastring(data_inicio_fase);
		}
		
		if (data_fim_fase){
			fase_atividade.data_fim = CommonsService.dataparastring(data_fim_fase)
		}
		
		$ctrl.alteracaodatafaseatividade();
		
	}
	
	$ctrl.adicionarprofissional = function (atividade) {
		var atividadeprofissional = {};
		if (!atividade.atividadeprofissionais) {
			atividade.atividadeprofissionais = [];
		}
		atividade.atividadeprofissionais.push(atividadeprofissional);
		
	}
	
	$ctrl.importaratividadesorcamento = function () {
		if ($ctrl.share.demanda.orcamento && 
				$ctrl.share.demanda.orcamento.orcamento_atividades){
			
			var fase_list = [];
			var fase_id_list = []
			
			if (!$ctrl.share.demanda.fase_atividades){
				$ctrl.share.demanda.fase_atividades = [];
			}
			
			
			for (let fase_atividade of $ctrl.share.demanda.fase_atividades) {
				if (fase_atividade.fase && fase_id_list.indexOf(fase_atividade.fase.id) < 0) {
					fase_list.push(fase_atividade.fase);
					fase_id_list.push(fase_atividade.fase.id);
				}
			}
			
			for (let orcamento_atividade of $ctrl.share.demanda.orcamento.orcamento_atividades) {
				if (orcamento_atividade.fase && fase_id_list.indexOf(orcamento_atividade.fase.id) < 0){
					fase_list.push(orcamento_atividade.fase);
					fase_id_list.push(orcamento_atividade.fase.id);
				}
			}
			
			var fase_atividades_list = [];
			
			for (let fase of fase_list) {
				var fase_atividade = {};

				var existe = false;
				for (let fa of $ctrl.share.demanda.fase_atividades){
					if (fa.fase.id == fase.id){
						fase_atividade = fa;
						existe = true;
					}
				}
				
				if (!existe){
					fase_atividades_list.push(fase_atividade);
					fase_atividade.fase = fase;
					
				}
				
				if (!fase_atividade.atividades){
					fase_atividade.atividades = [];
				}

				for (let orcamento_atividade of $ctrl.share.demanda.orcamento.orcamento_atividades) {
					if (orcamento_atividade.descricao && orcamento_atividade.fase){
						if (orcamento_atividade.fase.id == fase.id){
								var atividadeprofissional = {
									quantidade_horas: orcamento_atividade.total_horas
								}
								var atividade = {
									descricao: 	orcamento_atividade.descricao,
									atividadeprofissionais: [atividadeprofissional]
								}	
								fase_atividade.atividades.push(atividade);
						}
					}
				}
			}	
			
			$ctrl.share.demanda.fase_atividades = $ctrl.share.demanda.fase_atividades.concat(fase_atividades_list);
		}
	}
	
	$ctrl.modalatividademap = {};
	
	$ctrl.abrirmodalfuncionarios = atividade => {
		for(let key in $ctrl.modalatividademap){
			if (atividade.$$hashKey != key){
				$ctrl.modalatividademap[key] = {
					ativo: false
				};
			}
		}
		
		if (!$ctrl.modalatividademap[atividade.$$hashKey]) {
			$ctrl.modalatividademap[atividade.$$hashKey] = {
				ativo: false
			}
		}
		
		if (atividade.atividadeprofissionais){
			for (let atividadeprofissional of atividade.atividadeprofissionais) {
				if (!atividadeprofissional.remover){
					if (atividadeprofissional.pessoa_fisica) {
						$ctrl.modalatividademap[atividade.$$hashKey][atividadeprofissional.pessoa_fisica.id] = true;
					}
				}
			}
		}
		
		$ctrl.modalatividademap[atividade.$$hashKey].ativo = !$ctrl.modalatividademap[atividade.$$hashKey].ativo;
	}
	
	$ctrl.abrirmodaldatainicio = atividade => {
		if (!$ctrl.modalatividademap[atividade.$$hashKey]) {
			$ctrl.modalatividademap[atividade.$$hashKey] = {
				ativo: false
			}
		}
		
		$ctrl.modalatividademap[atividade.$$hashKey].data_inicio = !$ctrl.modalatividademap[atividade.$$hashKey].data_inicio
		
	}
	
	$ctrl.abrirmodaldatafim = atividade => {
		if (!$ctrl.modalatividademap[atividade.$$hashKey]) {
			$ctrl.modalatividademap[atividade.$$hashKey] = {
				ativo: false
			}
		}
		
		$ctrl.modalatividademap[atividade.$$hashKey].data_fim = !$ctrl.modalatividademap[atividade.$$hashKey].data_fim
		
	}
	
	$ctrl.adicionarremoverprofissional = (atividade, profissional) => {
		
		var atividadeprofissional = {};
		
		if (atividade.atividadeprofissionais && atividade.atividadeprofissionais.length > 0 && !atividade.atividadeprofissionais[0].pessoa_fisica){
			atividadeprofissional = atividade.atividadeprofissionais[0];
		} 
		
		if ($ctrl.modalatividademap[atividade.$$hashKey][profissional.id]) {
			
			if (!atividade.atividadeprofissionais){
				atividade.atividadeprofissionais = [];
			}
			
			atividadeprofissional.pessoa_fisica = profissional
			
			if (atividade.atividadeprofissionais.indexOf(atividadeprofissional) < 0){
				atividade.atividadeprofissionais.push(atividadeprofissional);
			}
			 
		} else {
			if (!atividade.atividadeprofissionais){
				atividade.atividadeprofissionais = [];
			}
			
			var atividadeprofissional = null;
			for(let ap of atividade.atividadeprofissionais){
				if (!ap.remover){
					if (ap.pessoa_fisica.id == profissional.id){
						atividadeprofissional = ap;
						break;
					}
				}
			}
			
			if (atividadeprofissional.id) {
				DemandaService.verificarseatividadeprofissionalpossuialocacao(atividadeprofissional.id, function (data){
					if (data.possui) {
						$ctrl.modalatividademap[atividade.$$hashKey][profissional.id] = true;
						alert('Não é permitido remover este profissional da atividade, pois ele já alocou horas.')
					} else {
						atividadeprofissional.remover=true
					}	
				});
			} else if (atividadeprofissional){
				atividadeprofissional.remover=true
			}
			
		}
		
	}
	
	$ctrl.fecharmodalfuncionario = atividade => {
		$ctrl.modalatividademap[atividade.$$hashKey].ativo = false;
	}
	
}).controller('ResumoController', function($rootScope, $scope, share, CommonsService ){
	var $ctrl = this;
	$ctrl.share = share;
	$scope.demanda = $ctrl.share.demanda;
	
	var configurarregistros = (data) => {
		for (let fase_atividade of data.fase_atividades) {
			for (let atividade of fase_atividade.atividades) {
				if (atividade.atividadeprofissionais){
					for (let atividade_profissional of atividade.atividadeprofissionais){
						if (atividade_profissional.horas_alocadas_milisegundos){
							atividade_profissional.horas_alocadas = CommonsService.milliparahoras(atividade_profissional.horas_alocadas_milisegundos);
						}
						
						if (atividade_profissional.quantidade_horas && atividade_profissional.quantidade_horas.toString().indexOf(':00') < 0){
							atividade_profissional.quantidade_horas_formatada = atividade_profissional.quantidade_horas + ':00';							
						}
					}
				}
			}
		}
	}
	
	if ($ctrl.share.demanda.$promise){
		$ctrl.share.demanda.$promise.then(function (data) {
			configurarregistros(data);
		});
	}
	
});

$(function(){
	  var hash = window.location.hash;
	  hash && $('ul.nav a[href="' + hash + '"]').tab('show');

	  $('.nav-tabs a').click(function (e) {
	    $(this).tab('show');
	    var scrollmem = $('body').scrollTop() || $('html').scrollTop();
	    window.location.hash = this.hash;
	    $('html,body').scrollTop(scrollmem);
	  });
	  
	  
	  $('li').on('click', function () {
		 if (!$('#dadosdemanda').hasClass('active')) {
			 $('#btnDeletar').css('display', 'none');
		 } else {
			 $('#btnDeletar').css('display', '');
		 }
	  });
	  
	  hash && hash != '#dadosdemanda' && $('#btnDeletar').css('display', 'none');
	  
});