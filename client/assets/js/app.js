(function () {
  var app = angular.module('invenco', [
    'ngRoute',
    'stocktaking.controllers',
    'datatables'
  ]);

  app.config(['$routeProvider', '$resourceProvider', function ($routeProvider, $resourceProvider) {
    $routeProvider
      .when('/marcas', {
        templateUrl: 'static/views/stocktaking/brands.html',
        controller: 'BrandController'
      })
      .when('/tipos', {
        templateUrl: 'static/views/stocktaking/types.html',
        controller: 'TypeController'
      })
      .when('/modelos', {
        templateUrl: 'static/views/stocktaking/models.html',
        controller: 'ModelController'
      })
      .when('/equipos', {
        templateUrl: 'static/views/stocktaking/equipments.html',
        controller: 'EquipmentController'
      });

    $resourceProvider.defaults.stripTrailingSlashes = false;
  }]);
})();
