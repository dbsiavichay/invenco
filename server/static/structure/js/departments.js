$(function () { 
	var id;

	$('.glyphicon-plus-sign').parent().on('click', function () {				
		openModal()
	});

	$('.glyphicon-pencil').parent().on('click', function () {
		id = $(this).parent().attr('id');
		$.get('/departments/'+id, function (object) {						
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
		makeRequest('/departments/', 'POST', getData(), reloadPage);
	});

	$('#btnEdit').on('click', function () {	
		var is_valid = validateForm();
		if(!is_valid) return;							
		makeRequest('/departments/'+id+'/', 'POST', getData(), reloadPage);
	});

	$('#btnDelete').on('click', function () {
		makeRequest('/departments/'+id+'/', 'DELETE', {}, reloadPage);
	});

	var reloadPage = function (data) {
		$(location).attr('href', '/departments/')
	}	
});