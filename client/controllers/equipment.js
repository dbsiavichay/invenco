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
  })

  .controller('ModelController', function ($scope, Model, Trademark, Type) {
    $scope.models = Model.query();
    $scope.types = Type.query();
    $scope.trademarks = Trademark.query();
    $scope.modelSpecifications = []
    $scope.modelOptions = []
    $scope.model = null;

    $scope.edit = function (model) {
      $scope.form.$setPristine();
      $scope.form.$setUntouched();
      $scope.formInline.$setPristine();
      $scope.formInline.$setUntouched();
      $scope.model = angular.copy(model) || new Model();

      renderSpecifications();
    }

    $scope.remove = function (model) {
      $scope.model = model;
      $('#deleteModal').modal('show');
    }

    $scope.reset = function () {
      $scope.model = null;
    }

    $scope.changeSpecifications = function () {
      $scope.modelSpecifications = [];
      $scope.modelOptions = [];
      var type_specifications = [];
      if($scope.model.type) type_specifications = angular.copy($scope.model.type.type_specifications);

      for(var i=0; i < type_specifications.length; i++) {
        if (type_specifications[i]['when'] != 'model') {
          type_specifications.splice(i, 1);
          i = i - 1;
        }
      }

      for(var i=0; i < type_specifications.length; i++) {
        var ts = type_specifications[i];
        if(!ts['options']) {
          angular.forEach(ts['name'].split(','), function (value) {
            $scope.modelSpecifications.push({
              'label' : value.trim(),
              'type' : 'text'
            });
          });
          type_specifications.splice(i, 1);
          i = i - 1;
        }
      }

      for(var i=0; i < type_specifications.length; i++) {
        var ts = type_specifications[i];

        if(ts['name'].indexOf('.') < 0) {
          var options = []

          angular.forEach(ts['options'].split(','), function (value) {
            options.push(value.trim());
          });

          $scope.modelSpecifications.push({
            'label': ts['name'],
            'type': 'select',
            'options': options
          });

          type_specifications.splice(i, 1);
          i = i - 1;
        }
      }

      for(var i=0; i < type_specifications.length; i++) {
        var ts = type_specifications[i];
        var label = ts['name'].split('.')[0];
        var actions = [];

        for(var j = i; j < type_specifications.length; j++){
          var _ts = type_specifications[j];

          if(_ts['name'].indexOf(label) > -1) {
            var options = []
            angular.forEach(_ts['options'].split(','), function (value) {
              options.push(value.trim());
            });

            actions.push({
              'name': _ts['name'].split('.')[1],
              'options': options
            });

            type_specifications.splice(j, 1);
            j = j - 1;
            i = j;
          }
        }

        $scope.modelSpecifications.push({
          'label' : label,
          'type' : 'select',
          'actions': actions
        });
      }

    }

    $scope.changeOptions = function (label, selected) {
      angular.forEach($scope.modelSpecifications, function (ms) {
        if(ms['label'] == label) {
          angular.forEach(ms['actions'], function (action) {
            if (action['name'] != selected) {
              angular.forEach(action['options'], function (option) {
                var index = $scope.modelOptions.indexOf(option);
                if (index > -1) $scope.modelOptions.splice(index, 1);
              });
            }
          });
          angular.forEach(ms['actions'], function (action) {
            if (action['name'] == selected) {
              angular.forEach(action['options'], function (option) {
                var index = $scope.modelOptions.indexOf(option);
                if (index < 0) $scope.modelOptions.push(option);
              });
            }
          });
          return;
        }
      });
    }

    $scope.create = function () {
      $scope.form.$setSubmitted();
      $scope.formInline.$setSubmitted();
      if(!$scope.form.$valid || !$scope.formInline.$valid) return;

      if(!$scope.model.specifications) $scope.model.specifications = []

      $scope.model
        .$save(function (response) {
          $scope.models.push($scope.model);
          $scope.reset();
        });
    }

    $scope.update = function () {
      $scope.form.$setSubmitted();
      $scope.formInline.$setSubmitted();
      if(!$scope.form.$valid || !$scope.formInline.$valid) return;

      $scope.model
        .$update(function (response) {
          var index = getIndex($scope.model);
          $scope.models[index] = angular.copy(response);
          $scope.reset();
        });
    }

    $scope.delete = function () {
      $scope.model
        .$remove(function () {
          var index = getIndex($scope.model);
          $scope.models.splice(index, 1);
          $scope.reset();
          $('#deleteModal').modal('hide');
        });
    }

    getIndex = function (model) {
      for(var i in $scope.models) {
        var t = $scope.models[i];
        if(t.id === model.id) return i;
      }
    }

    var renderSpecifications = function () {
      if($scope.model.type) {
        for (var i=0 in $scope.types) {
          var t = $scope.types[i];
          if($scope.model.type.id == t.id) {
            $scope.model.type = t
            break;
          }
        }
      }
      $scope.changeSpecifications();

      angular.forEach($scope.modelSpecifications, function (ms) {
        if(ms.actions) $scope.changeOptions(ms.label, $scope.model.specifications[ms.label]);
      });
    }
  })

  .controller('DeviceController', function ($scope, Device, Model, Trademark, Type) {
    $scope.devices = Device.query();
    $scope.types = Type.query();
    $scope.trademarks = Trademark.query();
    $scope.models = [];
    $scope.modelSpecifications = []
    $scope.modelOptions = []
    $scope.device = null;

    $scope.edit = function (device) {
      $scope.form.$setPristine();
      $scope.form.$setUntouched();
      $scope.formInline.$setPristine();
      $scope.formInline.$setUntouched();
      $scope.device = angular.copy(device) || new Device();

      //renderSpecifications();
    }

    $scope.remove = function (model) {
      $scope.model = model;
      $('#deleteModal').modal('show');
    }

    $scope.reset = function () {
      $scope.device = null;
    }

    $scope.changeModels = function () {
      var type = $scope.device.type.id
      $scope.models = Model.query({'type': type})
    }

    $scope.changeSpecifications = function () {
      $scope.modelSpecifications = [];
      $scope.modelOptions = [];
      var type_specifications = [];
      if($scope.model.type) type_specifications = angular.copy($scope.model.type.type_specifications);

      for(var i=0; i < type_specifications.length; i++) {
        if (type_specifications[i]['when'] != 'model') {
          type_specifications.splice(i, 1);
          i = i - 1;
        }
      }

      for(var i=0; i < type_specifications.length; i++) {
        var ts = type_specifications[i];
        if(!ts['options']) {
          angular.forEach(ts['name'].split(','), function (value) {
            $scope.modelSpecifications.push({
              'label' : value.trim(),
              'type' : 'text'
            });
          });
          type_specifications.splice(i, 1);
          i = i - 1;
        }
      }

      for(var i=0; i < type_specifications.length; i++) {
        var ts = type_specifications[i];

        if(ts['name'].indexOf('.') < 0) {
          var options = []

          angular.forEach(ts['options'].split(','), function (value) {
            options.push(value.trim());
          });

          $scope.modelSpecifications.push({
            'label': ts['name'],
            'type': 'select',
            'options': options
          });

          type_specifications.splice(i, 1);
          i = i - 1;
        }
      }

      for(var i=0; i < type_specifications.length; i++) {
        var ts = type_specifications[i];
        var label = ts['name'].split('.')[0];
        var actions = [];

        for(var j = i; j < type_specifications.length; j++){
          var _ts = type_specifications[j];

          if(_ts['name'].indexOf(label) > -1) {
            var options = []
            angular.forEach(_ts['options'].split(','), function (value) {
              options.push(value.trim());
            });

            actions.push({
              'name': _ts['name'].split('.')[1],
              'options': options
            });

            type_specifications.splice(j, 1);
            j = j - 1;
            i = j;
          }
        }

        $scope.modelSpecifications.push({
          'label' : label,
          'type' : 'select',
          'actions': actions
        });
      }

    }

    $scope.changeOptions = function (label, selected) {
      angular.forEach($scope.modelSpecifications, function (ms) {
        if(ms['label'] == label) {
          angular.forEach(ms['actions'], function (action) {
            if (action['name'] != selected) {
              angular.forEach(action['options'], function (option) {
                var index = $scope.modelOptions.indexOf(option);
                if (index > -1) $scope.modelOptions.splice(index, 1);
              });
            }
          });
          angular.forEach(ms['actions'], function (action) {
            if (action['name'] == selected) {
              angular.forEach(action['options'], function (option) {
                var index = $scope.modelOptions.indexOf(option);
                if (index < 0) $scope.modelOptions.push(option);
              });
            }
          });
          return;
        }
      });
    }

    $scope.create = function () {
      $scope.form.$setSubmitted();
      $scope.formInline.$setSubmitted();
      if(!$scope.form.$valid || !$scope.formInline.$valid) return;

      $scope.model
        .$save(function (response) {
          $scope.models.push($scope.model);
          $scope.reset();
        });
    }

    $scope.update = function () {
      $scope.form.$setSubmitted();
      $scope.formInline.$setSubmitted();
      if(!$scope.form.$valid || !$scope.formInline.$valid) return;

      $scope.model
        .$update(function (response) {
          var index = getIndex($scope.model);
          $scope.models[index] = angular.copy(response);
          $scope.reset();
        });
    }

    $scope.delete = function () {
      $scope.model
        .$remove(function () {
          var index = getIndex($scope.model);
          $scope.models.splice(index, 1);
          $scope.reset();
          $('#deleteModal').modal('hide');
        });
    }

    getIndex = function (model) {
      for(var i in $scope.models) {
        var t = $scope.models[i];
        if(t.id === model.id) return i;
      }
    }

    var renderSpecifications = function () {
      if($scope.model.type) {
        for (var i=0 in $scope.types) {
          var t = $scope.types[i];
          if($scope.model.type.id == t.id) {
            $scope.model.type = t
            break;
          }
        }
      }
      $scope.changeSpecifications();

      angular.forEach($scope.modelSpecifications, function (ms) {
        if(ms.actions) $scope.changeOptions(ms.label, $scope.model.specifications[ms.label]);
      });
    }
  });
})();
