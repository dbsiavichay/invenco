(function () {
  angular.module('equipment.services', [
    'ngResource',
  ])

  .factory('Trademark', function ($resource) {
    return $resource('/api/trademarks/:id/', {
      id: '@id'
    },{
      update: {method: 'PUT'}
    });
  })
  .factory('Type', function ($resource) {
    return $resource('/api/types/:id/', {
      id: '@id'
    },{
      update: {method: 'PUT'}
    })
  })
  .factory('Model', function ($resource) {
    return $resource('/api/models/:id/', {
      id: '@id'
    },{
      update: {method: 'PUT'}
    })
  });
})();
