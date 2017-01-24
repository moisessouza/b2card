"use strict";

var commons = angular.module('commons', ['ui.bootstrap',  'ngResource']);

var BASE_URL = '/'
var $scope_message = null;
var messages = {}

commons.directive('gbMoney', function () {
    return {
        require: '?ngModel',
        link: function (scope, elem, attrs, ctrl) {
            if (!ctrl) return;
            ctrl.$parsers.unshift(function (viewValue) {

          elem.priceFormat({
            prefix: '',
            centsSeparator: ',',
            thousandsSeparator: '.'
        });                

                return elem[0].value;
            });
        }
    };
}).directive('gbCnpj', function () {
    return {
        require: '?ngModel',
        link: function (scope, elem, attrs, ctrl) {
            if (!ctrl) return;
            $(elem).mask('99.999.999/9999-99');
        }
    };
}).directive('gbCep', function () {
    return {
        require: '?ngModel',
        link: function (scope, elem, attrs, ctrl) {
            if (!ctrl) return;
            $(elem).mask('99.999-999');
        }
    };
}).directive('gbData', function ($compile) {
    return {
        require: '?ngModel',
        link: function (scope, elem, attrs, ctrl) {
            if (!ctrl) return;
            //$(elem).mask('99/99/9999');
            input = elem.find('input').clone();
            input.setAttribute('ui-mask', '99/99/9999');
            input.setAttribute('model-view-value', 'true');
            input = $compile(input)(scope)
            elem.find('input').replaceWith(input);
        }
    };
}).directive('gbCpf', function () {
    return {
        require: '?ngModel',
        link: function (scope, elem, attrs, ctrl) {
            if (!ctrl) return;
            $(elem).mask('999.999.999-99');
        }
    };
}).directive('gbRg', function () {
    return {
        require: '?ngModel',
        link: function (scope, elem, attrs, ctrl) {
            if (!ctrl) return;
            $(elem).mask('aa-99.999.999');
        }
    };
}).service('CommonsService', function(){
	return {
		formatarnumero: function (numero) {
			if (numero || numero == 0) {
				return numero.toFixed(2).replace(/./g, function(c, i, a) {
					return i && c !== "." && ((a.length - i) % 3 === 0) ? '.' + c : c === "." ? ',' : c;
				}).replace('-.', '-');
			} else {
				return null;
			}
		},
		stringparafloat: function(string) {
			return parseFloat(string.replace(/\./g, '').replace(',','.'));
		},
		stringparadata: function (string) {
			var split = string.split('/');
			return new Date(split[2], split[1]-1, split[0]);
		},
		dataparastring: function(data){
			
			var dia = data.getDate() < 10 ? '0' + data.getDate() : data.getDate();
			var mes = (data.getMonth() + 1) < 10 ? '0' + (data.getMonth() + 1) : data.getMonth() + 1;
			var ano = data.getFullYear();
			
			return [dia, mes, ano].join('/');	
		},
		arredondar: function (numero){
			if (numero || numero == 0){
				return numero.toFixed(2);
			} else {
				return null;
			}
		},
		milliparahoras: function (milisegundos){
			var horas = parseInt(milisegundos/1000/60/60);
			var minutos = moment(milisegundos).minutes();
			horas = horas < 10 ? '0' + horas : horas;
			minutos = minutos < 10 ? '0' + minutos: minutos;
			return horas + ':' + minutos;
		}
	}
}).controller('MessageController', function ($scope){
	var $ctrl = this;
	$ctrl.show=true;
	$ctrl.messages = messages;
	$scope_message = $scope;
}).service('MessageService', function(){
	return {
		clear: function () {
			messages.clazz = null;	
			messages.message = null;
			$scope_message.$apply();
		},
		messageinfo: function (msg){
			messages.clazz = 'alert-warning';	
			messages.message = msg;
			$scope_message.$apply();
		},
		messagesuccess: function (msg) {
			messages.clazz = 'alert-success';
			messages.message = msg;
			$scope_message.$apply();
		}
	}
}).service('AutenticationService', function ($resource){
	return {
		buscarabasautorizadas(abas, callback){
			var Autentication = $resource(BASE_URL + 'autenticacao/api/permissoesaba/', {}, {
				'set': {method:'POST', isArray:true}
			});
			return Autentication.set({}, abas, callback);
		}
	}
});
