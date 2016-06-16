(function () {
  angular.module('equipment.controllers', [
    'equipment.services'
  ])

  .controller('TrademarkController', function ($scope, Trademark) {
    $scope.objectList = Trademark.query();
    
  });
})();
