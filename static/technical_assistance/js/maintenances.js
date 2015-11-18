$(function () { 
	var id, currentListboxItem;

	$('.glyphicon-plus-sign').parent().on('click', function () {				
		openModal()
	});

	$('.glyphicon-pencil').parent().on('click', function () {
		id = $(this).parent().attr('id');
		$.get('/jobs/'+id, function (object) {						
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
		makeRequest('/jobs/', 'POST', getData(), reloadPage);
	});

	$('#btnEdit').on('click', function () {		
		var is_valid = validateForm();
		if(!is_valid) return;		
		makeRequest('/jobs/'+id+'/', 'POST', getData(), reloadPage);
	});

	$('#btnDelete').on('click', function () {
		makeRequest('/jobs/'+id+'/', 'DELETE', {}, reloadPage);
	});	

	$('#search').on('keyup', function (event) {
		text = $('#search').val();
		//$('.well-listbox').find('a').show();
		$('.well-listbox').filter('a:contains("'+text+'")');
	});

	$('.well-listbox').find('a').on('click', function (event) {
		event.preventDefault();
		var check = '<span class="badge">'+
						'<span class="glyphicon glyphicon-check"></span>'+
					'</span>';
		if(currentListboxItem) currentListboxItem.find('.badge').remove();
		$(this).prepend(check);
		currentListboxItem = $(this);
	});

	var reloadPage = function (data) {
		$(location).attr('href', '/jobs/')
	}
});