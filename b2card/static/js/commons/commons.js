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
});
