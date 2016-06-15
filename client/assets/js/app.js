(function () {
  var app = angular.module('invenco', [
    'ngRoute',
    'controllers.trademark'
  ]);

  app.config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/marcas', {
        templateUrl: 'static/views/equipment/trademarks.html',
        controller: 'TrademarkController'
      });

  }]);
})();
