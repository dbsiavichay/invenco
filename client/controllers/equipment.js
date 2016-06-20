(function () {
  angular.module('equipment.controllers', [
    'equipment.services'
  ])

  .controller('TrademarkController', function ($scope, Trademark) {
    $scope.trademarks = Trademark.query();
    $scope.trademark = null;

    $scope.edit = function (trademark) {
      $scope.form.$setPristine();
      $scope.trademark = angular.copy(trademark) || new Trademark();
    }

    $scope.remove = function (trademark) {
      $scope.trademark = trademark;
      $('#deleteModal').modal('show');

    }

    $scope.reset = function () {
      $scope.trademark = null;
    }

    $scope.create = function () {
      if(!$scope.form.$valid) return;

      $scope.trademark
        .$save(function (response) {
          $scope.trademarks.push($scope.trademark);
          $scope.reset();
        });
    }

    $scope.update = function () {
      if(!$scope.form.$valid) return;

      $scope.trademark
        .$update(function (response) {
          var index = getIndex($scope.trademark);
          $scope.trademarks[index] = angular.copy(response);
          $scope.reset();
        });
    }

    $scope.delete = function () {
      $scope.trademark
        .$remove(function () {
          var index = getIndex($scope.trademark);
          $scope.trademarks.splice(index, 1);
          $scope.reset();
          $('#deleteModal').modal('hide');
        });
    }

    getIndex = function (trademark) {
      for(var i in $scope.trademarks) {
        var t = $scope.trademarks[i];
        if(t.id === trademark.id) return i;
      }
    }
  });
})();
