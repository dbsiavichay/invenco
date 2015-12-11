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
			$('#allocations-listbox').find('a[key='+object['device']+']').trigger('click');
			$('#parts-listbox').find('.added').remove();
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
		data['device'] = deviceSelected;
		data['parts'] = partsSelected.toString();
		makeRequest('/maintenances/'+id+'/', 'POST', data, reloadPage);
	});

	$('#btnDelete').on('click', function () {
		makeRequest('/jobs/'+id+'/', 'DELETE', {}, reloadPage);
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

	$('#allocations-listbox').find('a').on('click', function (event) {
		event.preventDefault();
		var check = '<span class="badge">'+
						'<span class="glyphicon glyphicon-check"></span>'+
					'</span>';
		$('#allocations-listbox').find('.badge').remove();
		$(this).prepend(check);		
	});

	$('#parts-listbox').find('a').on('click', function (event) {			
		event.preventDefault();
		checkPart($(this))
	});

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

	var reloadPage = function (data) {
		$(location).attr('href', '/maintenances/')
	}
});