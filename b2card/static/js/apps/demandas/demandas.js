"use strict";

var demandas = angular.module('demandas', ['demandas-services', 'pessoa-services', 'centrocusto-services', 'fase-services', 'valorhora-services', 'parcela', 'parcela-services',
                                           'centroresultado-services', 'unidadeadministrativa-services', 'ui.bootstrap', 'commons', 'ui.mask',  'ngMaterial']);

demandas.factory('share', function(){
	  return {};
});

demandas.controller('DemandaController', function ($rootScope, $scope, $window, $uibModal, $log, DemandaService, ParcelaService, PessoaService,
		CentroCustoService, ValorHoraService, CommonsService, AutenticationService, CentroResultadoService, UnidadeAdministrativaService, share, MessageService){
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
					return $ctrl.demanda;
				},
				listavalorhora: function () {
					return share.listavalorhora;
				}
				
			}
		});
			
		modalInstance.result.then(function(data) {
			configurardemanda($ctrl.demanda.id);
		}, function() {
			// $log.info('Modal dismissed at: ' + new Date());
		});
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
				
				$ctrl.listacentroresultadoshoras = DemandaService.buscarcentroresultadoshora(demanda_id);
				
			});
			
			share.demanda = $ctrl.demanda;
			
		} else {
			$ctrl.demanda = {
				'propostas':[{}],
				'tarefas':[{}],
				'observacoes':[{}],
				'ocorrencias':[{}],
				'orcamento': {},
				'atividades': [{}]
			}
			$ctrl.show=true;
			$ctrl.listacentroresultadoshoras = []
			share.demanda = $ctrl.demanda;
		}
	
	}
	
	configurardemanda(demanda_id);
	
	$ctrl.adicionarproposta = function () {
		$ctrl.demanda.propostas.unshift({});
	}
	
	$ctrl.adicionartarefa = function () {
		var tarefa = {'show': true};
		$ctrl.demanda.tarefas.unshift(tarefa);
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
	
	// TODO mudar isso depois... 
	share.listafuncionarios = $ctrl.listafuncionarios;
	
	$ctrl.listacentroresultados = CentroResultadoService.buscarcentroresultados();
	$ctrl.listaunidadeadministrativas = UnidadeAdministrativaService.buscarunidadeadministrativas();
	
	var abas = ['#dadosdemanda', '#orcamento', '#atividades', 
		'#proposta', '#tarefas', '#observacoes', '#ocorrencias']
	
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
		
		share.demanda.$promise.then(function (data) {
			$rootScope.$emit('orcamento', data);
			$rootScope.$emit('atividades', data);
		});
	}
	
	$ctrl.deletar = function () {
		DemandaService.deletardemanda($ctrl.demanda.id, function(data){
			$window.location.href = BASE_URL + 'demandas/';
		});
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
	
	$ctrl.retornarurl = function(url) {
		return BASE_URL + url +"?i=112";
	}
	
}).controller('OrcamentoController', function($rootScope, ValorHoraService, FaseService, CommonsService, share){
	var $ctrl = this;
	$ctrl.share = share;

	$ctrl.listavalorhorab2card = ValorHoraService.buscarvalorhorab2card();
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
			$rootScope.$emit('orcamento', data);
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
	
}).controller('AtividadeController', function(ValorHoraService, FaseService, CommonsService, PessoaService, share){
	var $ctrl = this;
	$ctrl.share = share;
	
	$ctrl.listafases = FaseService.buscarfases();
	var atividadeprofissional = {}
	
	$ctrl.remover = function (i, callback){
		i.remover = true;		
		if (callback){
			callback();
		}
	}
	
	$ctrl.share.demanda.atividades=[{
		atividadeprofissionais: [atividadeprofissional]
	}];
	
	$ctrl.atividadeprofissionalmap = {};
	$ctrl.atividadeprofissionalmap = {
		atividadeprofissional:[]
	}
	
	$ctrl.buscarprofissional = function (texto, atividadeprofissional){
		if (texto){
			PessoaService.buscarprofissional(texto, function (data){
				$ctrl.atividadeprofissionalmap[atividadeprofissional]=data;
			}); 
		}
	}
	
	$ctrl.adicionar = function () {
		var atividadeprofissional = {};
		$ctrl.share.demanda.atividades.push({
			atividadeprofissionais: [atividadeprofissional]
		});	
		
		$ctrl.atividadeprofissionalmap[atividadeprofissional] = [];
	}
	
	
	$ctrl.adicionarprofissional = function (atividade) {
		var atividadeprofissional = {};
		if (!atividade.atividadeprofissionais) {
			atividade.atividadeprofissionais = [];
		}
		atividade.atividadeprofissionais.push(atividadeprofissional);
		$ctrl.atividadeprofissionalmap[atividadeprofissional] = [];
	}
	
	$ctrl.importaratividadesorcamento = function () {
		if ($ctrl.share.demanda.orcamento && 
				$ctrl.share.demanda.orcamento.orcamento_atividades){
			
			for (let orcamento_atividade of $ctrl.share.demanda.orcamento.orcamento_atividades) {
				var atividadeprofissional = {
					quantidade_horas: orcamento_atividade.total_horas
				}
				$ctrl.atividadeprofissionalmap[atividadeprofissional] = [];
				var atividade = {
					fase: orcamento_atividade.fase,
					descricao: 	orcamento_atividade.descricao,
					atividadeprofissionais: [atividadeprofissional]
				}
				
				$ctrl.share.demanda.atividades.push(atividade);
				
			}
			
		}
		
		
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
});