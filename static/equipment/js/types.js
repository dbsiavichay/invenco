$(function () {
	var id;
	var specifications = [];
	addEventListenerOnNew();
	addEventListenerOnEdit();
	addEventListenerOnRemove();
	addEventListenerOnCreate();
	addEventListenerOnUpdate();
	addEventListenerOnDelete();
	addEventListenerOnAdd();
});

var getUrl = function () {
	return '/types/'
}

var addEventListenerOnNew = function () {
	$('.glyphicon-plus-sign').parent().on('click', function () {
		specifications = [];
		renderSpecifications(specifications)
		openModal()
	});
}

var addEventListenerOnEdit = function () {
	$('.glyphicon-pencil').parent().on('click', function () {
		id = $(this).parent().attr('id');
		$.get(getUrl()+id+'/', function (object) {
			specifications = object.specifications;
			renderSpecifications(specifications);
			openModal({'object':object});
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
		data['specifications'] = JSON.stringify(specifications);
		makeRequest(getUrl(), 'POST', data, reloadPage);
	});
}

var addEventListenerOnUpdate = function () {
	$('#btnEdit').on('click', function () {
		var is_valid = validateForm();
		if(!is_valid) return;
		var data = getData();
		data['specifications'] = JSON.stringify(specifications);
		if (data) makeRequest(getUrl()+id+'/', 'POST', data, reloadPage);
	});
}

var addEventListenerOnDelete = function () {
	$('#btnDelete').on('click', function () {
		makeRequest(getUrl()+id+'/', 'DELETE', {}, reloadPage);
	});
}

var addEventListenerOnAdd = function () {
	$('#btnAdd').on('click', function () {
		var specification_for = $('#inputSpecificationFor').find('input:checked');
		var specification_name = $('#inputSpecification');
		var specification_options = $('#inputOptions');
		var formSpecificationName = specification_name.parents('.form-group');

		if(formSpecificationName.hasClass('has-error')) formSpecificationName.removeClass('has-error');

		if(!specification_name.val().trim()) {
			formSpecificationName.addClass('has-error');
			return;
		}

		var item = getSpecification(specification_for.val(), specification_name.val(), specification_options.val());
		specifications.push(item);
		renderSpecifications(specifications);
	});
}

var renderSpecifications = function (detail) {
	var emptyTemplate = '<tr><td colspan="4">No existen registros</td></tr>';
	var tab = $('a[href=#detail]');
	var table = $('#table_detail');

	table.children().remove();

	if(detail.length) {
		for (var i in detail) {
			var item = detail[i];
			table.append(getTemplate(item['for'], JSON.stringify(item['specification']), JSON.stringify(item['options']), i));
		}
		tab.text('Detalle (' + detail.length + ')');
	}else{
		table.append(emptyTemplate);
		tab.text('Detalle');
	}

	$($('#inputSpecificationFor').find('input').get(0)).prop('checked', true);
	$('#inputSpecification').val('');
	$('#inputOptions').val('');

	addListenerDeleteSpecification();
}

var getTemplate = function (xor, specification, options, pos) {
	var template = '<tr>'+
						'<td class="col-xs-1">'+xor+'</td>'+
						'<td class="col-xs-5">'+specification+'</td>'+
						'<td class="col-xs-5">'+options+'</td>'+
						'<td class="col-xs-1">'+
							'<button id=detail-'+pos+' class="btn btn-sm btn-default btn-delete-specification">'+
								'<span class="glyphicon glyphicon-remove" aria-hidden="true"></span>'+
							'</button>'+
						'</td>'+
					'</tr>';
	return template;
}


var addListenerDeleteSpecification = function () {
	$('.btn-delete-specification').on('click', function () {
		var pos = $(this).attr('id').split('-')[1]
		specifications.splice(pos, 1);
		renderSpecifications(specifications);
	});
}


var getSpecification = function (strfor, strspecification, stroptions) {
	var item = {};

	var specification = splitByCommaToArray(strspecification);
	var options = getOptions(stroptions);

	item['for'] = strfor;
	item['specification'] = specification;
	item['options'] = options;

	return item;
}

var getOptions = function (str) {
	if(str.indexOf(':') < 0) return splitByCommaToArray(str);

	var options = [];
	var stroptions = str.split(';');

	for (var i in stroptions) {
		var option = {};
		stroptions[i] = stroptions[i].trim();
		if (stroptions[i]) {
			var name = stroptions[i].split(':')[0];
			var suboptions =  splitByCommaToArray(stroptions[i].split(':')[1])

			option['name'] = name;
			option['suboptions'] = suboptions;

			options.push(option);
		}
	}

	return options;
}


var splitByCommaToArray = function (str) {
	var values = str.split(',');
	for(var i in values) {
		values[i] = values[i].trim();
		if(!values[i]) values.splice(i, 1);
	}
	return values;
}

var reloadPage = function (data) {
	$(location).attr('href', getUrl());
}

//Funcionalidad para busquedas
var getRow = function (object) {
	var $row = $rowTemplate.clone();
	for (var attr in object) {
		if(attr=='id') {
			$row.find('[name=actions]').attr('id', object[attr])
		}else{
			$row.find('[name="'+attr+'"]').text(object[attr]);
		}
	}
	return $row;
}
