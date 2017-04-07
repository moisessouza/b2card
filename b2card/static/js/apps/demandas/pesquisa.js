"use strict";

var pesquisademanda = angular.module('pesquisademanda', ['pesquisademanda-services', 'pessoa-services', 'ui.bootstrap', 'commons', 'ui.mask', 'ngMaterial']);

pesquisademanda.controller('PesquisaDemandaController', function (CommonsService, MessageService, PesquisaDemandaService, PessoaService, $window){
	var $ctrl = this;
	$ctrl.show=true;
	
	var configurarresultado = function (resultado) {
		$ctrl.resultado = resultado;
		if (resultado.demandas) {
			for(let demanda of resultado.demandas) {
				demanda.descricao = CommonsService.pad(demanda.id, 5) + ' - ' + (demanda.unidade_administrativa ? demanda.unidade_administrativa.codigo : 'Sem UN') + ' - ' + demanda.cliente.nome_fantasia + ' - ' + demanda.codigo_demanda + ' - ' + demanda.nome_demanda;
			}
		}
	}
	
	$ctrl.listaclientes = PessoaService.buscarpessoasjuridicas();
	$ctrl.listaresponsaveis = PessoaService.buscargestores();
	
	$ctrl.arguments = {
		pagina: 1,
		ordenar: true
	}
	
	$ctrl.primeirapagina = () => {
		$ctrl.arguments.pagina = 1;
		$ctrl.pesquisar();
	}
	
	$ctrl.recuarpagina = () => {
		let pagina = $ctrl.arguments.pagina;
		pagina-=1;
		if (pagina < 1) {
			pagina = 1;
		}
		$ctrl.arguments.pagina = pagina;
		$ctrl.pesquisar();
	}
	
	$ctrl.avancarpagina = () => {
		let pagina = $ctrl.arguments.pagina;
		pagina+=1;
		if (pagina > $ctrl.resultado.total_paginas) {
			pagina = $ctrl.resultado.total_paginas;
		}
		$ctrl.arguments.pagina = pagina;	
		$ctrl.pesquisar();
	}
	
	$ctrl.ultimapagina = () => {
		$ctrl.arguments.pagina = $ctrl.resultado.total_paginas;
		$ctrl.pesquisar();
	}
	
	$ctrl.resultado = PesquisaDemandaService.buscardemandas($ctrl.arguments, configurarresultado);
	
	$ctrl.abrirmodalstatus = () => {
		$ctrl.showmodal = !$ctrl.showmodal; 
	}
	
	$ctrl.abrirmodalresponsaveis = () => {
		$ctrl.showmodalresponsaveis = !$ctrl.showmodalresponsaveis;
	}
	
	$ctrl.ordenar = () => {
		$ctrl.arguments.ordenar = !$ctrl.arguments.ordenar;
		$ctrl.pesquisar();
	}
	
	$ctrl.pesquisar = () => {
		
		if ($ctrl.arguments.data_inicio && $ctrl.arguments.data_fim) {
			
			let data_inicio;
			let data_fim;
			
			if ($ctrl.arguments.data_inicio instanceof Date) {
				data_inicio = $ctrl.arguments.data_inicio;
			} else {
				data_inicio = CommonsService.stringparadata($ctrl.arguments.data_inicio);
			}
			
			if ($ctrl.arguments.data_fim instanceof Date) {
				data_fim = $ctrl.arguments.data_fim;
			} else {
				data_fim = CommonsService.stringparadata($ctrl.arguments.data_fim);
			}
			
			if (data_inicio >= data_fim) {
				alert("Data fim deve ser maior que data inicio.");
				return;
			}
		}
		
		$ctrl.arguments.status = $ctrl.status;
		$ctrl.arguments.responsaveis = $ctrl.responsavel;
		PesquisaDemandaService.buscardemandas($ctrl.arguments, configurarresultado);
	}
	
	$ctrl.abrirdemanda = demanda => {
		$window.location.href = BASE_URL + 'demandas/editar/' + demanda.id;
	}
	
	$ctrl.novo = () => {
		$window.location.href = BASE_URL + 'demandas/novo/';
	}
	
	$ctrl.abrirdatainicio = () => {
		$ctrl.data_inicio = true;
	}
	
	$ctrl.abrirdatafim = () => {
		$ctrl.data_fim = true;
	}
	
});