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

pessoaservices.service('PessoaService', function($resource){
	return {
		
	}
});
