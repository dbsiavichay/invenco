(function () {
  var app = angular.module('invenco', [
    'ngRoute',
    'equipment.controllers',
    'datatables'
  ]);

  app.config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/marcas', {
        templateUrl: 'static/views/equipment/trademarks.html',
        controller: 'TrademarkController'
      });

  }]);
})();
