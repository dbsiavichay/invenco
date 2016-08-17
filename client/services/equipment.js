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
      query: {url: '/api/types/list/', method: 'GET', isArray: true},
      update: {method: 'PUT'}
    })
  })
  .factory('Model', function ($resource) {
    return $resource('/api/models/:id/', {
      id: '@id'
    },{
      query: {url: '/api/models/list/', method: 'GET', isArray: true},
      update: {method: 'PUT'},
      getFromList: {
        url: 'api/models/list/:id/',
        id: '@id',
        method: 'GET'
      }
    })
  })
  .factory('Device', function ($resource) {
    return $resource('/api/devices/:id/', {
      id: '@id'
    },{
      query: {url: '/api/devices/list/', method: 'GET', isArray: true},
      update: {method: 'PUT'},
      getFromList: {
        url: 'api/devices/list/:id/',
        id: '@id',
        method: 'GET'
      }
    })
  })
  .factory('Department', function ($resource) {
    return $resource('/api/departments/:id/', {
      id: '@id'
    })
  })
  .factory('Section', function ($resource) {
    return $resource('/api/sections/:id/', {
      id: '@id'
    })
  })
  .factory('Employee', function ($resource) {
    return $resource('/api/employees/:id/', {
      id: '@id'
    })
  })
  .factory('Assignment', function ($resource) {
    return $resource('/api/allocations/:id/', {
      id: '@id'
    })
  });
})();
