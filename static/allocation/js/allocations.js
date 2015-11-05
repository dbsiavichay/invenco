$(function () {
	$('.selectpicker').selectpicker();
	$('.datepicker').datepicker({
	    autoclose: true,
	    format: 'yyyy-mm-dd'
	});

	var id;
	var equipments = [];

	$('.glyphicon-plus-sign').parent().on('click', function () {
		equipments = [];
		var $table = $('#table_detail');
		var $tab = $('a[href=#summary]');
		$table.find('tr[class!=empty]').remove();
		$table.children().show();
		$tab.text('Resumen');
		$('.nav-tabs').find('a').show();
		$('#tab-from').hide();
		$('#tab-employee').tab('show');
		openModal()
	});

	$('.btn-transfer').on('click', function () {
		id = $(this).parent().attr('id');
		$.get('/allocations/'+id+'/')
		.then(function (object) {
			return $.get('/allocations/?employee='+object['employee']);
		})
		.then(function (devices) {
			renderDevices(devices);
			$('.nav-tabs').find('a').show();
			$('#tab-equipment').hide();
			$('#tab-summary').hide();
			$('#tab-from').tab('show');			
			openModal({'date_joined': ''});
		});
	});

	$('.glyphicon-remove').parent().on('click', function () {
		id = $(this).parent().attr('id');		
		$('#objectDeleteModal').modal('show');
	});

	$('#btnSave').on('click', function () {
		$('.alert').hide();		
		var is_valid = validateForm();
		var has_allocations = equipments.length > 0;
		if(!has_allocations) {
			$('#inputDevice').parents('.form-group').addClass('has-error');
			return;
		}
		if(!is_valid) return;
		var requests = [];
		var data = getData($('#employee'));
		for (var i in equipments) {
			data['device'] = equipments[i];
			data['is_active'] = true;			
			var request = $.ajax({
		        url: '/allocations/',        
		        method: 'POST', 
		        data: data,
		        dataType: 'json'	        
		    });
		    requests.push(request);
 		}
		$.when(requests).then(function () {
			reloadPage();
		});
	});

	$('#btnEdit').on('click', function () {
		var is_valid = validateForm();
		if(!is_valid) return;

		var requests = [];
		var data = getData($('#employee'));
		var table = $('#table_devices');
		table.find('input[type=checkbox]:checked')
		.each(function (index, item) {
			var pk =  $(item).attr('pk');
			var device = $(item).val();
			data['is_active'] = true;
			data['device'] = device;
			var request = $.ajax({
		        url: '/allocations/'+pk+'/',        
		        method: 'POST', 
		        data: data,
		        dataType: 'json'	        
		    });		
		    requests.push(request);
		});

		$.when(requests)
		.then(function () {
			reloadPage();
		});		
	});

	$('#btnDelete').on('click', function () {
		makeRequest('/allocations/'+id+'/', 'DELETE', {}, reloadPage);
	});

	$('#btnAdd').on('click', function () {
		renderSummary();
	});

	$('#inputType').on('change', function () {
		getDevices();	
	});

	$('#inputDepartment').on('change', function () {		
		getAreas();
	});

	$('#inputArea').on('change', function () {		
		getEmployees();
	});

	var getDevices = function () {
		var type = $('#inputType').val();
		$.get('/devices/?type='+type)
		.then(function (data) {
			$('#inputDevice').children().remove();    	
	    	for(var i in data) {
	    		var device = data[i];
	    		var disabled = equipments.indexOf(device['id']) >= 0?'disabled':'';	    		
	    		var option = '<option '+disabled+' value="'+device['id']+'">'+device['code']+' | '+device['type'] +' '+device['trademark']+' '+device['model']+'</option>';
	    		$('#inputDevice').append(option);
	    	}
	    	$('#inputDevice').selectpicker('refresh');
		});
	}

	var getAreas = function () {
		var department = $('#inputDepartment').val();
		if (!department) return;
		$.get('/areas/?department='+department)
		.then(function (data) {
			$('#inputArea').find("option[value!='']").remove();    	
			$('#inputEmployee').find("option[value!='']").remove();
	    	for(var i in data) {
	    		var department = data[i];
	    		var option = '<option value="'+department['id']+'">'+department['name']+'</option>';
	    		$('#inputArea').append(option);
	    	}
	    	$('#inputArea').selectpicker('refresh');
	    	$('#inputEmployee').selectpicker('refresh')
		});
	}

	var getEmployees = function () {
		var area = $('#inputArea').val();
		if (!area) return;
		$.get('/employees/?area='+area)
		.then(function (data) {			
			$('#inputEmployee').find("option[value!='']").remove();    	
	    	for(var i in data) {
	    		var employee = data[i];
	    		var option = '<option value="'+employee['id']+'">'+employee['charter']+' | '+employee['full_name']+'</option>';
	    		$('#inputEmployee').append(option);
	    	}
	    	$('#inputEmployee').selectpicker('refresh');
		});
	}

	var renderSummary = function () {
		var items = $('#inputDevice').val();		
		var tab = $('a[href=#summary]');
		var table = $('#table_detail');

		$('#inputType').parents('.form-group').removeClass('has-error');
		$('#inputDevice').parents('.form-group').removeClass('has-error');		

		if(items) {
			table.find('.empty').hide();
			for (var i in items) {
				var pk = items[i];
				var name = $('#inputDevice').find('option[value='+pk+']').text();				
				table.append(getTemplate(pk, name));
				equipments.push(parseInt(pk));
			}	
			tab.text('Resumen (' + equipments.length + ')');
		}else{
			var type = $('#inputType').val();
			if (!type) $('#inputType').parents('.form-group').addClass('has-error');
			$('#inputDevice').parents('.form-group').addClass('has-error');
			return;
		}

		$('#inputType').selectpicker('val', '');
		$('#inputDevice').find('option[value!=""]').remove();
		$('#inputDevice').selectpicker('refresh')

		addEventDeleteListener();
	}

	var getTemplate = function (pk, name) {
		var template =  '<tr pk="'+pk+'">'+
							'<td class="col-xs-11">'+name+'</td>'+							
							'<td class="col-xs-1">'+
								'<button class="btn btn-sm btn-default btn-delete-device">'+
									'<span class="glyphicon glyphicon-remove" aria-hidden="true"></span>'+
								'</button>'+
							'</td>'+
						'</tr>';
		return template;
	}

	var addEventDeleteListener = function () {
		$('.btn-delete-device').on('click', function () {
			var tab = $('a[href=#summary]');
			var pk = $(this).parents('tr').attr('pk');
			$(this).parents('tr').remove();
			equipments.splice(equipments.indexOf(pk), 1);
			if(equipments.length > 0) {
				tab.text('Resumen ('+equipments.length+')');	
			} else {
				tab.text('Resumen')	
				$('#table_detail').find('.empty').show();	
			} 
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

	var reloadPage = function (data) {
		$(location).attr('href', '/allocations/')
	}	
});