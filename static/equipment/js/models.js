$(function () {
	var initilizeSelectPicker = function () {		
		$('.selectpicker').selectpicker();
	}

	initilizeSelectPicker();

	var modelId;
	var modelTypeField = $('#selType');
	var modelTrademarkField = $('selTrademark');
	var modelNameField = $('#txtName');
	var modelSpecificationsField = [];	


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


	modelTypeField.on('change', function () {
		var idType = modelTypeField.val();
		var request = $.ajax({
	        url: '/types/'+idType+'/',     
	        method: 'GET',
	        dataType: 'json'	        
	    });

	    request.done(function (data) {	    	
	    	var specifications = data.specifications;
	    	var form = $('#form-specifications');
			form.children().remove();

	    	for (var i in specifications) {
	    		if (specifications[i]['for']==='model') {
	    			renderSpecification(form, specifications[i].specification, specifications[i].options);
	    		}
	    		initilizeSelectPicker();
	    	}
	    });
	});


	var renderSpecification = function (form, specification, options) {
		if(specification.length < 1) return;
		if(specification.length > 1) {
			for(var i in specification) {
				form.append(getTextElement(specification[i]));
			}
		}else{
			if(options.length < 1) {
				form.append(getTextElement(specification[0]))
			}else{						
				form.append(getSelectElement(specification[0], options));				
			}
		}
	}


	var getTextElement = function (name) {
		var template =  '<div class="form-group">'+
						    '<label for="txt'+name.capitalize()+'" class="col-md-2 control-label">'+name.capitalize()+'</label>'+
						    '<div class="col-md-10">'+
						        '<input id="txt'+name.capitalize()+'" type="text" class="form-control">'+
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
			optionElements = optionElements + getItemSelectElement(option);
		}
		
		template =  '<div class="form-group">'+
						    '<label for="sel'+name.capitalize()+'" class="col-md-2 control-label">'+name.capitalize()+'</label>'+
						    '<div class="col-md-10">'+
						        '<select id="sel'+name.capitalize()+'" class="form-control selectpicker" data-size="10" data-live-search="true">'+
						        	'<option value="">--- Seleccionar ---</option>'+
									optionElements+						        	
						        '</select>'+
						    '</div>'+
						'</div>';
		return template;
	}

	var getItemSelectElement = function (name) {
		var template = '<option value="'+name.capitalize()+'">'+name.capitalize()+'</option>';
		return template;
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


	var getSpecifications = function (strfor, strspecification, stroptions) {
		var item = {};

		var specification = splitByCommaToArray(strspecification);
		var options = getOptions(stroptions);

		item['for'] = strfor;
		item['specification'] = specification;
		item['options'] = options;

		return item;
	}


	var splitByCommaToArray = function (str) {		
		var values = str.split(',');
		for(var i in values) {
			values[i] = values[i].trim();
			if(!values[i]) values.splice(i, 1);
		}
		return values;
	}	


	var openTypeModal = function (model) {
		cleanErrorForm()

		$('input:radio[name=optSpecificationFor][value=model]').prop('checked', true);
		$('#txtSpecification').val('');
		$('#txtOptions').val('');		
		if (model) {			
			modelNameField.val(model.name);
			modelSpecificationsField = model.specifications;
			$('#btnEdit').show();
			$('#btnSave').hide();
		} else {
			modelNameField.val('');
			$('#btnEdit').hide();
			$('#btnSave').show();
		}		

		//renderDetail(modelSpecificationsField);		
		$('#objectModal').modal('show');
	}

	var cleanErrorForm = function () {
		var nameFormGroup = modelNameField.parents('.form-group');		
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