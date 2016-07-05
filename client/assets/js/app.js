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
      })
      .when('/tipos', {
        templateUrl: 'static/views/equipment/types.html',
        controller: 'TypeController'
      })
      .when('/modelos', {
        templateUrl: 'static/views/equipment/models.html',
        controller: 'ModelController'
      })
      .when('/dispositivos', {
        templateUrl: 'static/views/equipment/devices.html',
        controller: 'DeviceController'
      });

    $resourceProvider.defaults.stripTrailingSlashes = false;
  }]);
})();
