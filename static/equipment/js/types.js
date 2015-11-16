$(function () {	
	var id;	
	var specifications = [];

	$('.glyphicon-plus-sign').parent().on('click', function () {
		specifications = [];
		renderSpecifications(specifications)				
		openModal()
	});

	$('.glyphicon-pencil').parent().on('click', function () {
		id = $(this).parent().attr('id');
		$.get('/types/'+id+'/', function (object) {
			specifications = object.specifications;
			renderSpecifications(specifications);
			openModal(object);
		});
	});

	$('.glyphicon-remove').parent().on('click', function () {
		id = $(this).parent().attr('id');		
		$('#objectDeleteModal').modal('show');
	});


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


	$('#btnSave').on('click', function () {	
		var is_valid = validateForm();
		if(!is_valid) return;		
		var data = getData();
		data['specifications'] = JSON.stringify(specifications);	
		makeRequest('/types/', 'POST', data, reloadPage);
	});

	$('#btnEdit').on('click', function () {		
		var is_valid = validateForm();
		if(!is_valid) return;		
		var data = getData();
		data['specifications'] = JSON.stringify(specifications);		
		if (data) makeRequest('/types/'+id+'/', 'POST', data, reloadPage);
	});

	$('#btnDelete').on('click', function () {
		makeRequest('/types/'+id+'/', 'DELETE', {}, reloadPage);
	});

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
		$(location).attr('href', '/types/');
	}	
});