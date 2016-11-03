var commons = angular.module('commons', ['ui.bootstrap']);

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
}).directive('gbData', function () {
    return {
        require: '?ngModel',
        link: function (scope, elem, attrs, ctrl) {
            if (!ctrl) return;
            $(elem).mask('99/99/9999');
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
			return numero.toFixed(2).replace(/./g, function(c, i, a) {
			    return i && c !== "." && ((a.length - i) % 3 === 0) ? '.' + c : c === "." ? ',' : c;
			})
		}
	}
});
