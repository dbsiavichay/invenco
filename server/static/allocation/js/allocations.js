$(function () {
	var id;
	var equipments = [];

	initSelectPicker();
	initDatePicker();
	addEventListenerOnNew();
	addEventListenerOnEdit();
	addEventListenerOnRemove();
	addEventListenerOnCreate();
	addEventListenerOnCreateOther();
	addEventListenerOnUpdate();
	addEventListenerOnDelete();
	addEventChangeListenerOnType();
	addEventChangeListenerOnDepartment();

	makeRequest('/employees/', 'GET', {}, renderEmployees);
});

var getUrl = function () {
	return '/allocations/';
}

var initSelectPicker = function () {
	$('.selectpicker').selectpicker({
		showSubtext: true
	});
}

var initDatePicker = function () {
	$('.datepicker').datepicker({
			autoclose: true,
			format: 'yyyy-mm-dd'
	});
}

var addEventListenerOnNew = function () {
	$('.glyphicon-plus-sign').parent().on('click', function () {
		equipments = [];
		$('#form-specifications').children().remove();
		$('#form-suboptions').children().remove();
		$('#empty-specifications').show();
		$('#btnSaveOther').show();
		openModal({'tabs':[2,3,4]})
	});
}

var addEventListenerOnView = function () {
	$('.glyphicon-search').parent().on('click', function () {
		var deviceId = $(this).attr('dev-id');
		$.get('/devices/'+deviceId+'/')
		.then(function (data) {
			$('.detail-item:not([style])').remove();
			var $temp = $('.detail-item').clone().removeAttr('style');

			var $li = $temp.clone()
			$li.find('.key > strong').text('Tipo');
			$li.find('.value').text(data['type_name']);
			$('.detail-list').append($li);

			$li = $temp.clone()
			$li.find('.key > strong').text('Modelo');
			$li.find('.value').text(data['model_name']);
			$('.detail-list').append($li);

			$li = $temp.clone()
			$li.find('.key > strong').text('Codigo');
			$li.find('.value').text(data['code']);
			$('.detail-list').append($li);

			$li = $temp.clone()
			$li.find('.key > strong').text('Serial');
			$li.find('.value').text(data['serial']);
			$('.detail-list').append($li);

			for (attr in data['model_specifications']) {
				$li = $temp.clone()
				$li.find('.key > strong').text(attr);
				$li.find('.value').text(data['model_specifications'][attr]);
				$('.detail-list').append($li);
			}

			for (attr in data['specifications']) {
				$li = $temp.clone()
				$li.find('.key > strong').text(attr);
				$li.find('.value').text(data['specifications'][attr]);
				$('.detail-list').append($li);
			}

			$('#equipmentDetail').modal('show');
		});
	});
}

var addEventListenerOnEdit = function () {
	addEventListenerOnView()

	$('.btn-transfer').on('click', function () {
		id = $(this).parent().attr('id');
		$.get(getUrl()+id+'/')
		.then(function (object) {
			return $.get('/allocations/?employee='+object['employee']);
		})
		.then(function (devices) {
			renderDevices(devices);
			$('#btnSaveOther').hide();
			object = {'date_joined': ''}
			openModal({'object': object, 'tabs':[1,2]});
		});
	});
}

var addEventListenerOnRemove = function () {
	$('.glyphicon-remove').parent().on('click', function () {
		id = $(this).parent().attr('id');
		$('#objectDeleteModal').modal('show');
	});
}

var addEventListenerOnCreate = function () {
	$('#btnSave').on('click', function () {
		var is_valid = validateForm();

		if(!is_valid) return;

		var data = getData();
		var specifications = JSON.stringify(getData($('#specifications')));
		data['department'] = parseFloat(data['department']);
		data['area'] = parseFloat(data['area']);
		data['is_active'] = true;
		data['specifications'] = specifications;

		makeRequest(getUrl(), 'POST', data, reloadPage);
	});
}

var addEventListenerOnCreateOther = function () {
	$('#btnSaveOther').on('click', function () {
		var is_valid = validateForm();

		if(!is_valid) return;

		var data = getData();
		var specifications = JSON.stringify(getData($('#specifications')));
		data['department'] = parseFloat(data['department']);
		data['area'] = parseFloat(data['area']);
		data['is_active'] = true;
		data['specifications'] = specifications;

		makeRequest(getUrl(), 'POST', data, function () {
			$('#inputType').selectpicker('val', '');
			$('#inputDevice').selectpicker('val', '');
			$('#form-specifications').children().remove();
			$('#form-suboptions').children().remove();
			$('#empty-specifications').show();
			$('#tab-equipment').tab('show');
		});
	});
}

var addEventListenerOnUpdate = function () {
	$('#btnEdit').on('click', function () {
		var is_valid = validateForm('#employee');
		if(!is_valid) return;

		var requests = [];
		var data = getData($('#employee'));
		data['department'] = parseFloat(data['department']);
		data['area'] = parseFloat(data['area']);
		var table = $('#table_devices');
		table.find('input[type=checkbox]:checked')
		.each(function (index, item) {
			var pk =  $(item).attr('pk');
			var device = $(item).val();
			data['is_active'] = true;
			data['device'] = device;
			var request = $.ajax({
						url: getUrl()+pk+'/',
						method: 'POST',
						data: data,
						dataType: 'json'
				});
				requests.push(request);
		});

		$.when(requests)
		.done(function () {
			reloadPage();
		});
	});
}

var addEventListenerOnDelete = function () {
	$('#btnDelete').on('click', function () {
		makeRequest(getUrl()+id+'/', 'DELETE', {}, reloadPage);
	});
}

var addEventChangeListenerOnType = function () {
	$('#inputType').on('change', function () {
		getDevices();
		renderSpecifications();
	});
}

var addEventChangeListenerOnDepartment = function () {
	$('#inputDepartment').on('change', function () {
		getAreas();
	});
}

var getDevices = function () {
	var type = $('#inputType').val();
	$.get('/devices/?type='+type)
	.then(function (data) {
		$('#inputDevice').children().remove();
			for(var i in data) {
				var device = data[i];
				var added = equipments.indexOf(device['id']) >= 0?' disabled data-subtext="Agregado" ':'';
				var asiggned = device['is_assigned']?'disabled':'';
				var subtext = device['subtext']?'data-subtext="'+ device['subtext'] + '"':'';
				var option = '<option '+asiggned+' '+subtext+ added +' value="'+device['id']+'">'+device['code']+' | '+device['type'] +' '+device['trademark']+' '+device['model']+'</option>';
				$('#inputDevice').append(option);
			}
			$('#inputDevice').selectpicker('refresh');
	});
}

var getAreas = function () {
	var department = $('#inputDepartment').val();
	if (!department) return;
	$.get('/sections/?department='+parseInt(department))
	.then(function (data) {
		$('#inputArea').find("option[value!='']").remove();
			for(var i in data) {
				var area = data[i];
				var option = '<option value="'+area['code']+'">'+area['name']+'</option>';
				$('#inputArea').append(option);
			}
			$('#inputArea').selectpicker('refresh');
	});
}

var renderDevices = function (items) {
	var table = $('#table_devices');
	table.children().remove();
	for (var i in items) {
		var item = items[i];
		var checked = parseInt(id)===item['id']?'checked':'';
		var template =  '<tr>'+
							'<td class="col-xs-11">'+item['code']+' | '+item['name']+'</td>'+
							'<td class="col-xs-1">'+
								'<div class="checkbox">'+
										'<label>'+
											'<input pk="'+item['id']+'" value="'+item['device']+'" type="checkbox" '+checked+'>'+
										'</label>'+
								'</div>'+
							'</td>'+
						'</tr>';
		if(checked) table.prepend(template);
		else table.append(template);
	}
}

var renderSpecifications = function (object) {
	var type = $('#inputType').val();

	var request = $.get('/types/'+type+'/')
		.then(function (data) {
			var specifications = data.specifications;
			var form = $('#form-specifications');
			var empty = true;
		form.children().remove();
			$('#empty-specifications').hide();

		if(!specifications) {
			console.log(specifications);
			form.append('<p><em>"No existen especificaciones para este dispositivo"</em></p>');
			return;
		}

			for (var i in specifications) {
				var item = specifications[i];
				if (item['for']==='allocation') {
					empty = false;
					var elements = getSpecificationElements(item['specification'], item['options']);
					form.append(elements);
					initSelectPicker();
				}
			}

			if (empty) $('#empty-specifications').show();

			if(object) setFormValues(object);
		})
		.then(function () {
			return addEventChanceListener();
		})
		.then(function (selects) {
			if(object) selects.trigger('change');
			return $.get('/models/?type='+type)
		})
		.then(function (data) {
			$('#inputModel').find("option[value!='']").remove();
			for(var i in data) {
				var model = data[i];
				var option = '<option value="'+model['id']+'">'+model['name']+'</option>';
				$('#inputModel').append(option);
			}
			$('#inputModel').selectpicker('refresh');
			if (object) setFormValues(object);
		});
}

var addEventChanceListener = function () {
	var selects = $('#form-specifications').find('[type=select]');

	selects.on('change', function () {
		var form = $('#form-suboptions');
		var value = $(this).val();
		if (value) {
			var option = $(this).find("option[value='"+value+"']");
			var str = option.attr('suboptions').trim();
			if(str) {
				form.children().remove();
				var suboptions = str.split(',');
				for (var i in suboptions) {
					form.append(getTextElement(suboptions[i]));
				}
			}
		}else{
			form.children().remove();
		}
	});

	return selects;
}

var getSpecificationElements = function (specification, options) {
	if(specification.length < 1) return;

	if(specification.length > 1) {
		var array = [];
		for(var i in specification) {
			array.push(getTextElement(specification[i]));
		}
		return array;
	}else{
		if(options.length < 1) {
			return getTextElement(specification[0]);
		}else{
			return getSelectElement(specification[0], options);
		}
	}
}

var getTextElement = function (name) {
	var template =  '<div class="form-group">'+
							'<label for="input'+name.capitalize()+'" class="col-md-2 control-label">'+name.capitalize()+'</label>'+
							'<div class="col-md-10">'+
									'<input id="input'+name.capitalize()+'" name="'+name+'" type="text" class="form-control" req="true">'+
							'</div>'+
					'</div>'

	return template;
}

var getSelectElement = function (name, options) {
	var template = '';
	var optionElements = '';
	var is_object = options[0] instanceof Object;

	for (var i in options) {
		var option = is_object?options[i]['name']:options[i];
		var suboptions = is_object?options[i]['suboptions'].toString():'';
		optionElements = optionElements + getItemSelectElement(option, suboptions);
	}

	template =  '<div class="form-group">'+
						'<label for="input'+name.capitalize()+'" class="col-md-2 control-label">'+name.capitalize()+'</label>'+
						'<div class="col-md-10">'+
								'<select id="input'+name.capitalize()+'" name="'+name+'" type="select" class="form-control selectpicker" data-size="10" data-live-search="true" req="true">'+
									'<option value="">--- Seleccionar ---</option>'+
							optionElements+
								'</select>'+
						'</div>'+
				'</div>';
	return template;
}

var getItemSelectElement = function (name, suboptions) {
	var template = '<option suboptions="'+suboptions+'" value="'+name.capitalize()+'">'+name.capitalize()+'</option>';
	return template;
}

var reloadPage = function (data) {
	$(location).attr('href', getUrl())
}

var renderEmployees = function (data) {
	$('#inputEmployee').find("option[value!='']").remove();
	for(var i in data) {
		var employee = data[i];
		var option = '<option value="'+employee['charter']+'">'+employee['charter']+ ' | ' +employee['fullname']+'</option>';
		$('#inputEmployee').append(option);
	}
	$('#inputEmployee').selectpicker('refresh');
}

//Funcionalidad para busquedas
var getRow = function (object) {
	var $row = $rowTemplate.clone();
	for (var attr in object) {
		if(attr=='id') {
			$row.find('[name=actions]').attr('id', object[attr]);
			$row.find('[name=actions] button').first().attr('dev-id', object['device']);
		} else if (attr == 'state') {
			var $icon = $row.find('.glyphicon[name=state]');
			if ($icon.hasClass('glyphicon-ok-sign')) $icon.removeClass('glyphicon-ok-sign');
			if ($icon.hasClass('glyphicon-minus-sign')) $icon.removeClass('glyphicon-minus-sign');
			if ($icon.hasClass('glyphicon-remove-sign')) $icon.removeClass('glyphicon-remove-sign')
			$icon.addClass(object['state']);
		}else{
			$row.find('[name="'+attr+'"]').text(object[attr]);
		}
	}
	return $row;
}