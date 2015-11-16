$(function () {
	var id;

	$('.glyphicon-plus-sign').parent().on('click', function () {				
		openModal()
	});

	$('.glyphicon-pencil').parent().on('click', function () {
		id = $(this).parent().attr('id');
		$.get('/providers/'+id, function (object) {						
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
		makeRequest('/providers/', 'POST', getData(), reloadPage);
	});

	$('#btnEdit').on('click', function () {		
		var is_valid = validateForm();
		if(!is_valid) return;
		makeRequest('/providers/'+id+'/', 'POST', getData(), reloadPage);
	});

	$('#btnDelete').on('click', function () {
		makeRequest('/providers/'+id+'/', 'DELETE', {}, reloadPage);
	});

	var reloadPage = function (data) {
		$(location).attr('href', '/providers/')
	}	
});