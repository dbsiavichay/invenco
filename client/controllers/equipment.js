(function () {
  angular.module('equipment.controllers', [
    'equipment.services'
  ])

  .controller('TrademarkController', function ($location, $scope, Trademark) {
    $scope.objectList = Trademark.query();
    $scope.edit = false;

    $scope.add = function () {
      $scope.edit = true;
    }
  });
})();
