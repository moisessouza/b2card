"use strict";

var pessoaservices = angular.module('pessoa-services', ['ngResource']);

pessoaservices.config(['$resourceProvider', function($resourceProvider) {
	  // Don't strip trailing slashes from calculated URLs
	  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

pessoaservices.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

pessoaservices.service('PessoaService', function($resource, $http){
	return {
		buscarpessoas: function () {
			var Pessoa = $resource(BASE_URL + 'cadastros/pessoa/api/list');
			return Pessoa.query();
		},
		buscarpessoa: function (pessoa_id, callback){
			var Pessoa = $resource(BASE_URL + 'cadastros/pessoa/api/:id');
			return Pessoa.get({id:pessoa_id}, callback);
		},
		salvarpessoa: function (pessoa, callback) {
			var Pessoa = $resource(BASE_URL + 'cadastros/pessoa/api/new/');
			return Pessoa.save({}, pessoa, callback);
		},
		deletarpessoa: function (pessoa_id, callback) {
			var Pessoa = $resource(BASE_URL + 'cadastros/pessoa/api/:id');
			return Pessoa.remove({id:pessoa_id}, {}, callback);
		},
		buscarpessoasjuridicas: function (callback){
			var PessoaJuridica = $resource(BASE_URL + 'cadastros/pessoa/api/pessoajuridica/list/');
			return PessoaJuridica.query(callback);
		},
		buscarclientes: function (callback){
			var PessoaJuridica = $resource(BASE_URL + 'cadastros/pessoa/api/pessoajuridica/clientes/');
			return PessoaJuridica.query(callback);
		},
		buscarprofissionais: function(callback){
			var Pessoa = $resource(BASE_URL + 'cadastros/pessoa/api/pessoafisica/list/');
			return Pessoa.query(callback);
		},
		buscarprofissional: function(texto, callback){
			var Pessoa = $resource(BASE_URL + 'cadastros/pessoa/api/pessoafisica/:texto/');
			return Pessoa.query({'texto': texto}, {}, callback);
		},
		buscargestores: function(callback) {
			var Pessoa = $resource(BASE_URL + 'cadastros/pessoa/api/gestores/');
			return Pessoa.query(callback)
		},
		uploadfile: function(pessoa_juridica_id, callback) {
			
			var formData = new FormData();
			var file = document.getElementById('file');
            formData.append('file', file.files[0], file.files[0].name);
            
            $http({
                url: BASE_URL + 'cadastros/pessoa/api/pessoajuridica/uploadarquivo/' + pessoa_juridica_id + '/',
                method: "POST",
                data: formData,
                headers: {'Content-Type': undefined}
            }).success(function (response) {
                callback(response);
            });
            
		},
		removerarquivo: function(pessoa_juridica_id, callback) {
			var Arquivo = $resource(BASE_URL + 'cadastros/pessoa/api/pessoajuridica/removerarquivo/:pessoa_juridica_id/')
			return Arquivo.get({'pessoa_juridica_id': pessoa_juridica_id}, callback)
		}
	}
});
