$(function () {
	var id;	

	var initilizeSelectPicker = function () {		
		$('.selectpicker').selectpicker();
	}

	$('.datepicker').datepicker({
	    autoclose: true,
	    format: 'yyyy-mm-dd'
	});

	initilizeSelectPicker();


	$('.glyphicon-plus-sign').parent().on('click', function () {
		$('#form-specifications').children().remove();	
		$('#form-suboptions').children().remove();
		$('#empty-specifications').show();
		openModal()
	});

	$('.glyphicon-pencil').parent().on('click', function () {
		id = $(this).parent().attr('id');
		$.get('/devices/'+id+'/', function (object) {
			for(attr in object.specifications) {
				object[attr] = object.specifications[attr];
			}
			setFormValues(object);
			renderSpecifications(object);
			openModal(object);
		});
	});

	$('.glyphicon-remove').parent().on('click', function () {
		id = $(this).parent().attr('id');		
		$('#objectDeleteModal').modal('show');
	});

	$('#btnSave').on('click', function () {		
		var is_valid = validateForm();
		if(!is_valid) return;
		var data = getData($('#general'));
		data['specifications'] = JSON.stringify(getData($('#specifications')));
		makeRequest('/devices/', 'POST', data, reloadPage);
	});

	$('#btnEdit').on('click', function () {		
		var is_valid = validateForm();
		if(!is_valid) return;
		var data = getData($('#general'));
		data['specifications'] = JSON.stringify(getData($('#specifications')));
		makeRequest('/devices/'+id+'/', 'POST', data, reloadPage);
	});

	$('#btnDelete').on('click', function () {
		makeRequest('/devices/'+id+'/', 'DELETE', {}, reloadPage);
	});

	$('#inputType').on('change', function () {
		renderSpecifications();		
	});

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
	    		if (item['for']==='device') {
	    			empty = false;
	    			var elements = getSpecificationElements(item['specification'], item['options']);
	    			form.append(elements);
	    			initilizeSelectPicker();	    			
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
		$(location).attr('href', '/devices/');
	}
});