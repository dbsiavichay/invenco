(function () {
  angular.module('equipment.services', [
    'ngResource',
  ])

  .factory('Trademark', function ($resource) {
    return $resource('/api/trademarks/');
  });
})();
