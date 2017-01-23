"use strict";

var pessoa = angular.module('pessoa', ['pessoa-services', 'centrocusto-services','centroresultado-services', 
    'contagerencial-services',	'naturezaoperacao-services', 'recursos-services', 'commons', 'ui.bootstrap', 'ui.mask']);

pessoa.controller('PessoaController', function ($scope, $window, $uibModal, PessoaService, CentroCustoService, 
		CentroResultadoService, ContaGerencialService, NaturezaOperacaoService, AutenticationService, MessageService, CommonsService, RecursosService){
	var $ctrl = this;
	
	if (pessoa_id) {
		$ctrl.pessoa = PessoaService.buscarpessoa(pessoa_id, function (pessoa) {
			RecursosService.buscarusuariosnaousados(function (data){
				$ctrl.listausuarios = data;
				if (pessoa.pessoa_fisica){
					if(pessoa.pessoa_fisica.prestadores){
						for(let prestador of pessoa.pessoa_fisica.prestadores){
							RecursosService.buscarusuarioprestador(prestador.id, function (data){
								$ctrl.listausuarios = $ctrl.listausuarios.concat(data);
							});
						}
					}
					if (pessoa.pessoa_fisica.custos_prestador){
						for(let custo_prestador of pessoa.pessoa_fisica.custos_prestador){
							custo_prestador.valor = CommonsService.formatarnumero(custo_prestador.valor);
						}
					}
				}
			});
		});
	} else {
		$ctrl.pessoa = {
			status: 'A',
			pessoa_juridica: {
				contatos: []
			}
		}
		$ctrl.listausuarios = RecursosService.buscarusuariosnaousados();
	}
	
	$ctrl.centroresultadolist = CentroResultadoService.buscarcentroresultados();
	$ctrl.contagerenciallist = ContaGerencialService.buscarcontagerenciais();
	$ctrl.naturezaoperacaolist = NaturezaOperacaoService.buscarnaturezaoperacoes();
	$ctrl.listacargos = RecursosService.buscarcargos();
	$ctrl.listacentrocusto = CentroCustoService.buscarcentrocustos();
	$ctrl.listapessoasjuridicas = PessoaService.buscarpessoasjuridicas();
	
	var abas = ['#dadoscadastro', '#endereco', '#telefone', '#dadosbancarios', 
		'#telefonecontato', '#dadosprestador', '#apropriacoes', '#custoprestador']
	
	$ctrl.listaabasautorizadas = AutenticationService.buscarabasautorizadas(abas, function (){
		$ctrl.show = true;
	});
	
	$ctrl.adicionarendereco = function () {
		if(!$ctrl.pessoa.enderecos){
			$ctrl.pessoa.enderecos = [];
		}
		$ctrl.pessoa.enderecos.push({});
	}
	
	$ctrl.adicionartelefone = function () {
		if (!$ctrl.pessoa.telefones) {
			$ctrl.pessoa.telefones = [];
		}
		$ctrl.pessoa.telefones.push({});
	}
	
	$ctrl.adicionardadosbancarios = function () {
		if(!$ctrl.pessoa.dados_bancarios){
			$ctrl.pessoa.dados_bancarios = [];
		}
		$ctrl.pessoa.dados_bancarios.push({});
	}
	
	$ctrl.remover = function (objeto, lista) {
		objeto.remover=true;
	}
	
	$ctrl.adicionarprestador = function () {
		if (!$ctrl.pessoa.pessoa_fisica.prestadores){
			$ctrl.pessoa.pessoa_fisica.prestadores = [];
		}
		
		$ctrl.pessoa.pessoa_fisica.prestadores.push({});
		
	}
	
	$ctrl.adicionarcustoprestador = function(){
		if(!$ctrl.pessoa.pessoa_fisica.custos_prestador){
			$ctrl.pessoa.pessoa_fisica.custos_prestador = [];
		}
		
		$ctrl.pessoa.pessoa_fisica.custos_prestador.push({});
	}
	
	$ctrl.adicionarcontato = function () {
		
		if(!$ctrl.pessoa.pessoa_juridica) {
			$ctrl.pessoa.pessoa_juridica = {
				contatos: []
			}
		}
		
		if (!$ctrl.pessoa.pessoa_juridica.contatos){
			$ctrl.pessoa.pessoa_juridica.contatos = [];
		}
		
		$ctrl.pessoa.pessoa_juridica.contatos.push({
			telefones:[{}]
		});
	}
	
	$ctrl.adicionartelefonecontato = function(contato){
		contato.telefones.push({});
	}
	
	$ctrl.salvar = function () {
		MessageService.clear();
		$ctrl.pessoa = PessoaService.salvarpessoa($ctrl.pessoa, function (pessoa) {
			if (pessoa.pessoa_fisica){
				if (pessoa.pessoa_fisica.custos_prestador){
					for(let custo_prestador of pessoa.pessoa_fisica.custos_prestador){
						custo_prestador.valor = CommonsService.formatarnumero(custo_prestador.valor);
					}
				}
			}
			MessageService.messagesuccess('Cadastro realizado com sucesso!');
		});
	}
	
	$ctrl.deletarpessoa = function (){
		PessoaService.deletarpessoa($ctrl.pessoa.id, function () {
			$window.location.href = BASE_URL + 'cadastros/pessoa/';
		});
	}
	
	$ctrl.changenumeroconta = function (dado_bancario){
		dado_bancario.cod_agencia = dado_bancario.cod_agencia.replace(/[^0-9\-]/g, '');
	}
	
	
	$ctrl.open = function (size, parentSelector) {
	    var modalInstance = $uibModal.open({
	      animation: $ctrl.animationsEnabled,
	      ariaLabelledBy: 'modal-title',
	      ariaDescribedBy: 'modal-body',
	      templateUrl: 'myModalContent.html',
	      controller: 'ModalInstanceCtrl',
	      controllerAs: '$ctrl',
	      size: size,
	      resolve: {
	        demanda: function () {
	          return $scope.demanda;
	        }
	      }
	    });
	    
	    modalInstance.result.then(function (proposta) {
	    	$ctrl.listacargos = RecursosService.buscarcargos();
	    }, function () {
	        //$log.info('Modal dismissed at: ' + new Date());
	    });
	};
	
	$ctrl.datasvalidas = true;
	$ctrl.datascustovalidas = true;
	
	$ctrl.validardataprestador = function (prestador) {
		
		if(!prestador.data_inicio){
			return;
		}
		
		MessageService.clear();
		$ctrl.datasvalidas = true;
		
		var datainicio = CommonsService.stringparadata(prestador.data_inicio);
		var datafim = prestador.data_fim ? CommonsService.stringparadata(prestador.data_fim) : null;
		
		if (datafim && datainicio >= datafim) {
			$ctrl.datasvalidas = false;
		} else if ($ctrl.pessoa.pessoa_fisica.prestadores) {
			for(let prestador_list of $ctrl.pessoa.pessoa_fisica.prestadores) {
				if (prestador_list != prestador){
					var datainiciolist = prestador_list.data_inicio;
					var datafimlist = prestador_list.data_fim;
					
					datainiciolist = CommonsService.stringparadata(datainiciolist)
					datafimlist = datafimlist ? CommonsService.stringparadata(datafimlist) : null
							
					if(!datafimlist && !datafim){
						$ctrl.datasvalidas = false;
					}
					
					if (datainicio >= datainiciolist && datainicio <= datafimlist){
						$ctrl.datasvalidas = false;
					}
					
					if(datafim && datafimlist) {
						if (datafim >= datainiciolist && datafim <= datafimlist){
							$ctrl.datasvalidas = false;
						}
						if (datainicio >= datainiciolist && datafim <=datafimlist){
							$ctrl.datasvalidas = false;
						}
					}
					
				}
			}
		}
		
		if (!$ctrl.datasvalidas) {
			MessageService.messageinfo('Certifique-se que as datas de vigência do prestador estão corretas.')
		}
		
	}
	
	
	$ctrl.validardatacusto = function (custo) {
		
		if(!custo.data_inicio){
			return;
		}
		
		MessageService.clear();
		$ctrl.datascustovalidas = true;
		
		var datainicio = CommonsService.stringparadata(custo.data_inicio);
		var datafim = custo.data_fim ? CommonsService.stringparadata(custo.data_fim) : null;
		
		if (datafim && datainicio >= datafim) {
			$ctrl.datascustovalidas = false;
		} else if ($ctrl.pessoa.pessoa_fisica.custos_prestador) {
			for(let custo_list of $ctrl.pessoa.pessoa_fisica.custos_prestador) {
				if (custo_list != custo){
					var datainiciolist = custo_list.data_inicio;
					var datafimlist = custo_list.data_fim;
					
					datainiciolist = CommonsService.stringparadata(datainiciolist)
					datafimlist = datafimlist ? CommonsService.stringparadata(datafimlist) : null
							
					if(!datafimlist && !datafim){
						$ctrl.datascustovalidas = false;
					}
					
					if (datainicio >= datainiciolist && datainicio <= datafimlist){
						$ctrl.datascustovalidas = false;
					}
					
					if(datafim && datafimlist) {
						if (datafim >= datainiciolist && datafim <= datafimlist){
							$ctrl.datascustovalidas = false;
						}
						if (datainicio >= datainiciolist && datafim <=datafimlist){
							$ctrl.datascustovalidas = false;
						}
					}
					
				}
			}
		}
		
		if (!$ctrl.datascustovalidas) {
			MessageService.messageinfo('Certifique-se que as datas de vigência do custo do prestador estão corretas.')
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
	
	
}).controller('ListPessoaController', function ($scope, $window, PessoaService){
	var $ctrl = this;
	$ctrl.show = true;
	
	$ctrl.pessoas = PessoaService.buscarpessoas();
	
	$ctrl.redirecionar = function (pessoa) {
		$window.location.href = BASE_URL + 'cadastros/pessoa/editar/' + pessoa.id
	}
	
}).controller('ModalInstanceCtrl', function($scope, $uibModalInstance, RecursosService){
	
	var $ctrl = this;
	
	$ctrl.listacargos = RecursosService.buscarcargos();
	
	$ctrl.salvar = function () {
		
		if (!$ctrl.cargo)
			$ctrl.cargo = {}
		
		$ctrl.cargo.nome_cargo = $ctrl.nome_cargo;
		$ctrl.cargo.gestor = $ctrl.gestor;
		RecursosService.salvarcargo($ctrl.cargo, function (data){
			if (!$ctrl.cargo.edit){
				$ctrl.listacargos.push(data);
			}
			$ctrl.cargo = {}
			$ctrl.nome_cargo = "";
			$ctrl.gestor = false;
		});
	}
	
	$ctrl.deletar = function () {
		RecursosService.deletarcargo($ctrl.cargo, function (data){
			$ctrl.listacargos.splice($ctrl.listacargos.indexOf($ctrl.cargo), 1);
			$ctrl.cargo = {}
			$ctrl.nome_cargo = "";
			$ctrl.gestor = false;
		});
	}
	
	$ctrl.edit = function (cargo) {
		$ctrl.cargo = cargo;
		$ctrl.cargo.edit=true;
		$ctrl.nome_cargo = cargo.nome_cargo;
		$ctrl.gestor = cargo.gestor;
	}
	
	$ctrl.close = function () {
	   $uibModalInstance.close({});
	};
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