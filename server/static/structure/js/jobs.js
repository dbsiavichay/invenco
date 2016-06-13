$(function () { 
	var id;

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

	var reloadPage = function (data) {
		$(location).attr('href', '/jobs/')
	}
});