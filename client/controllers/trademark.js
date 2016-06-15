(function () {
  angular.module('controllers.trademark', [])
    .controller('TrademarkController', [
      '$scope',
      '$http',
      function ($scope, $http) {
        $scope.objectList = [];
        $http.get('/api/marcas/')
          .then(function (response) {
            console.log(response);
            $scope.objectList = response.data;
          });
      }]);
})();
