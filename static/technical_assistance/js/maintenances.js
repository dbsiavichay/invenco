$(function () {
	$.expr[":"].contains = $.expr.createPseudo(function(arg) {
	    return function( elem ) {
	        return $(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
	    };
	});

	$('.datepicker').datepicker({
	    autoclose: true,
	    format: 'yyyy-mm-dd'
	});

	var id

	$('.glyphicon-plus-sign').parent().on('click', function () {
		$('#error-equipment').hide();
		$('#allocations-listbox').find('.badge').remove();
		$('#parts-listbox').find('.badge').remove();
		$('#parts-listbox').find('.added').remove();
		$('#parts-count').text('0');
		openModal()
	});

	$('.glyphicon-pencil').parent().on('click', function () {
		id = $(this).parent().attr('id');
		$.get('/maintenances/'+id+'/', function (object) {
			var item = $('#allocations-listbox').find('a[key='+object['device']+']').trigger('click');
			$('#allocations-listbox > .list-group').prepend(item.remove());
			$('#parts-listbox').find('.added').remove();
			addClickEventListenerOnDevices();
			renderSelectedParts(object['parts']);
			openModal({'object': object});
		});
	});

	$('.glyphicon-remove').parent().on('click', function () {
		id = $(this).parent().attr('id');
		$('#objectDeleteModal').modal('show');
	});

	$('#btnSave').on('click', function () {
		var deviceSelected, partsSelected = [], data;
		var is_valid = validateForm();
		if(!is_valid) return;
		deviceSelected = $('#allocations-listbox').find('.badge').parent().attr('key');

		if(!deviceSelected) {
			$('#error-equipment').show();
			var tab = $('.nav-tabs').find('a')[0];
			$(tab).tab('show');
			return;
		}

		$('#parts-listbox').find('.badge')
		.parent().each(function (index, item) {
			var part = $(item).attr('key');
			partsSelected.push(parseInt(part));
		});

		data = getData();
		data['device'] = deviceSelected;
		data['parts'] = partsSelected.toString();
		data['specifications'] = JSON.stringify(getData($('#specifications')));
		makeRequest('/maintenances/', 'POST', data, reloadPage);
	});

	$('#btnEdit').on('click', function () {
		var deviceSelected, partsSelected = [], data;
		var is_valid = validateForm();
		if(!is_valid) return;
		deviceSelected = $('#allocations-listbox').find('.badge').parent().attr('key');

		$('#parts-listbox').find('.badge')
		.parent().each(function (index, item) {
			var part = $(item).attr('key');
			partsSelected.push(parseInt(part));
		});

		data = getData();
		data['specifications'] = JSON.stringify(getData($('#specifications')));
		data['device'] = deviceSelected;
		data['parts'] = partsSelected.toString();
		makeRequest('/maintenances/'+id+'/', 'POST', data, reloadPage);
	});

	$('#btnDelete').on('click', function () {
		makeRequest('/maintenances/'+id+'/', 'DELETE', {}, reloadPage);
	});

	$('#search-allocations').on('keyup', function (event) {
		text = $(this).val();
		$('#allocations-listbox').find('a').show();
		$('#allocations-listbox').find('a').filter('a:not(:contains("'+text+'"))').hide();
	});

	$('#search-parts').on('keyup', function (event) {
		text = $(this).val();
		$('#parts-listbox').find('a').show();
		$('#parts-listbox').find('a').filter('a:not(:contains("'+text+'"))').hide();
	});

	$('#parts-listbox').find('a').on('click', function (event) {
		event.preventDefault();
		checkPart($(this))
	});

	$('#parts-listbox').find('a').on('mouseover', function () {
		var data = $(this).attr('data');
		$('#parts-detail').text(data);
	});

	var addClickEventListenerOnDevices = function () {
		$('#allocations-listbox').find('a').on('click', function (event) {
			event.preventDefault();
			var device = $(this).attr('key');
			var check = '<span class="badge">'+
							'<span class="glyphicon glyphicon-check"></span>'+
						'</span>';
			$('#allocations-listbox').find('.badge').remove();
			$(this).prepend(check);
			renderSpecifications(device);
		});
	}

	var checkPart = function ($button) {
		var check = '<span class="badge">'+
						'<span class="glyphicon glyphicon-check"></span>'+
					'</span>';
		var badges = $button.find('.badge');
		if(badges.length > 0) badges.remove();
		else $button.prepend(check);
		var count = $('#parts-listbox').find('.badge').length;
		$('#parts-count').text(count);
	}

	var renderSelectedParts = function (parts) {
		for (var index in parts) {
			part = parts[index];
			var template = '<a href="#" key="'+part['part']+'" class="list-group-item added">'+
								'<span class="badge">'+
									'<span class="glyphicon glyphicon-check"></span>'+
								'</span>'+
							    part['name']+
							'</a>';
			$('#parts-listbox').find('.list-group').prepend(template);
			$('#parts-listbox').find('a[key='+part['part']+']').on('click', function (event) {
				event.preventDefault();
				checkPart($(this));
			});
		}
	}

	var renderSpecifications = function (device) {
		var object;
		var request = $.get('/devices/'+device+'/')
			.then(function (data) {
				object = data['specifications'];
				return $.get('/types/'+data['type']+'/');
			})
			.then(function (data) {
				var specifications = data.specifications;
				var form = $('#form-specifications');
				var empty = true;
			form.children().remove();
				$('#empty-specifications').hide();

			if(!specifications) {
				form.append('<p><em>"No existen especificaciones para este dispositivo"</em></p>');
				return;
			}

				for (var i in specifications) {
					var item = specifications[i];
					if(object) {
						if (item['for']==='device' || item['for']==='allocation') {
							empty = false;
							var elements = getSpecificationElements(item['specification'], item['options']);
							form.append(elements);
							initilizeSelectPicker();
						}
					}else {
						if (item['for']==='device') {
							empty = false;
							var elements = getSpecificationElements(item['specification'], item['options']);
							form.append(elements);
							initilizeSelectPicker();
						}
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

	var initilizeSelectPicker = function () {
		$('.selectpicker').selectpicker();
	}

	var reloadPage = function (data) {
		$(location).attr('href', '/maintenances/')
	}

	addClickEventListenerOnDevices();
});
