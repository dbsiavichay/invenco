(function () {
  angular.module('equipment.controllers', [
    'equipment.services'
  ])

  .controller('TrademarkController', function ($scope, Trademark) {
    $scope.trademarks = Trademark.query();
    $scope.trademark = null;

    $scope.edit = function (trademark) {
      $scope.form.$setPristine();
      $scope.form.$setUntouched();
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
  })

  .controller('TypeController', function ($scope, Type) {
    $scope.types = Type.query();
    $scope.type = null;
    $scope.specifications = [{}];

    $scope.edit = function (type) {
      $scope.form.$setPristine();
      $scope.form.$setUntouched();
      $scope.formInline.$submitted=false;

      $scope.type = angular.copy(type) || new Type();
      $scope.specifications = type?angular.copy($scope.type.type_specifications):[{}];
      if(!$scope.specifications.length) $scope.specifications.push({})
    }

    $scope.remove = function (type) {
      $scope.type = type;
      $('#deleteModal').modal('show');
    }

    $scope.reset = function () {
      $scope.type = null;
    }

    $scope.addSpecification = function () {
      $scope.specifications.push({});
    }

    $scope.removeSpecification = function (index) {
      $scope.specifications.splice(index,1);
    }

    $scope.create = function () {
      $scope.formInline.$setSubmitted();
      if(!$scope.form.$valid || !validateSpecifications()) return;

      $scope.type
        .$save(function (response) {
          $scope.types.push($scope.type);
          $scope.reset();
        });
    }

    $scope.update = function () {
      $scope.formInline.$setSubmitted();
      if(!$scope.form.$valid || !validateSpecifications()) return;

      $scope.type
        .$update(function (response) {
          var index = getIndex($scope.type);
          $scope.types[index] = angular.copy(response);
          $scope.reset();
        });
    }

    $scope.delete = function () {
      $scope.type
        .$remove(function () {
          var index = getIndex($scope.type);
          $scope.types.splice(index, 1);
          $scope.reset();
          $('#deleteModal').modal('hide');
        });
    }

    getIndex = function (type) {
      for(var i in $scope.types) {
        var t = $scope.types[i];
        if(t.id === type.id) return i;
      }
    }

    validateSpecifications = function () {
      $scope.type.type_specifications = [];
      for(var i = 0; i < $scope.specifications.length; i++){
        var s = $scope.specifications[i];

        if ((s.when && !s.name) || (!s.when && s.name)) return false;
        else if (s.when && s.name) $scope.type.type_specifications.push(s);
      }

      return true;
    }

  });
})();
