$(function () {	
	var typeId;
	var typeNameField = $('#txtName');
	var typeSpecificationsField = [];	


	$('.glyphicon-plus-sign').parent().on('click', function () {
		typeSpecificationsField = [];				
		openTypeModal()
	});

	$('.glyphicon-pencil').parent().on('click', function () {
		typeId = $(this).parent().attr('id');
		$.get('/types/'+typeId, function (type) {
			openTypeModal(type);
		});
	});

	$('.glyphicon-remove').parent().on('click', function () {
		typeId = $(this).parent().attr('id');		
		$('#objectDeleteModal').modal('show');
	});

	$('#btnAdd').on('click', function () {
		var specification_for = $('input:radio[name=optSpecificationFor]:checked');
		var specification_name = $('#txtSpecification');
		var specification_options = $('#txtOptions');
		var formSpecificationName = specification_name.parents('.form-group');

		if(formSpecificationName.hasClass('has-error')) formSpecificationName.removeClass('has-error');

		if(!specification_name.val().trim()) {			
			formSpecificationName.addClass('has-error');
			return;
		}		

		var item = getSpecification(specification_for.val(), specification_name.val(), specification_options.val());
		typeSpecificationsField.push(item);
		renderDetail(typeSpecificationsField);
	});	



	$('#btnSave').on('click', function () {		
		var data = getData();		
		if (data) makeRequest('/types/', 'POST', data);
	});

	$('#btnEdit').on('click', function () {		
		var data = getData();		
		if (data) makeRequest('/types/'+data.id+'/', 'POST', data);
	});

	$('#btnDelete').on('click', function () {
		makeRequest('/types/'+typeId+'/', 'DELETE', {});
	});

	var renderDetail = function (detail) {
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

		$('input:radio[name=optSpecificationFor][value=model]').prop('checked', true);
		$('#txtSpecification').val('');
		$('#txtOptions').val('');

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
			typeSpecificationsField.splice(pos, 1);
			renderDetail(typeSpecificationsField);
		});
	}


	var getData = function () {
		var id = parseInt(typeId);
		var name = typeNameField.val();
		var specifications = JSON.stringify(typeSpecificationsField);
		var is_valid = true;

		cleanErrorForm()		

		if (!name) {
			typeNameField.parents('.form-group').addClass('has-error');
			is_valid = false;
		}

		if (is_valid) {
			var data = {
				id: id,				
				name: name,
				specifications: specifications
			}
			return data;			
		}
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


	var openTypeModal = function (type) {
		cleanErrorForm()

		$('input:radio[name=optSpecificationFor][value=model]').prop('checked', true);
		$('#txtSpecification').val('');
		$('#txtOptions').val('');		
		if (type) {			
			typeNameField.val(type.name);
			typeSpecificationsField = type.specifications;
			$('#btnEdit').show();
			$('#btnSave').hide();
		} else {
			typeNameField.val('');
			$('#btnEdit').hide();
			$('#btnSave').show();
		}		

		renderDetail(typeSpecificationsField);		
		$('#objectModal').modal('show');
	}

	var cleanErrorForm = function () {
		var nameFormGroup = typeNameField.parents('.form-group');		
		var specificationFormGroup = $('#txtSpecification').parents('.form-group');
		if (nameFormGroup.hasClass('has-error')) nameFormGroup.removeClass('has-error');
		if (specificationFormGroup.hasClass('has-error')) specificationFormGroup.removeClass('has-error');		
	}


	var makeRequest = function (url, method, data) {
		var request = $.ajax({
	        url: url,        
	        method: method, 
	        data: data,
	        dataType: 'json'	        
	    });

	    request.done(function (data) {	    	
	    	$(location).attr('href', '/types/');
	    });

	    request.error(function (error) {
	    	console.log(error);
	    });
	}		
});