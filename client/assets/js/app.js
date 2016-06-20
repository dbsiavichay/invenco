(function () {
  var app = angular.module('invenco', [
    'ngRoute',
    'equipment.controllers',
    'datatables'
  ]);

  app.config(['$routeProvider', '$resourceProvider', function ($routeProvider, $resourceProvider) {
    $routeProvider
      .when('/marcas', {
        templateUrl: 'static/views/equipment/trademarks.html',
        controller: 'TrademarkController'
      });

    $resourceProvider.defaults.stripTrailingSlashes = false;
  }]);
})();
