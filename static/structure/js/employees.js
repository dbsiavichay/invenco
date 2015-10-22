$(function () {
	$('.selectpicker').selectpicker();

	var id;

	$('.glyphicon-plus-sign').parent().on('click', function () {				
		openModal()
	});

	$('.glyphicon-pencil').parent().on('click', function () {
		id = $(this).parent().attr('id');
		$.get('/employees/'+id+'/', function (object) {
			setFormValues(object);
			getAreas(object);
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
		makeRequest('/employees/', 'POST', getData(), reloadPage);
	});

	$('#btnEdit').on('click', function () {		
		var is_valid = validateForm();
		if(!is_valid) return;
		makeRequest('/employees/'+id+'/', 'POST', getData(), reloadPage);
	});

	$('#btnDelete').on('click', function () {
		makeRequest('/employees/'+id+'/', 'DELETE', {}, reloadPage);
	});

	$('#inputDepartment').on('change', function () {		
		getAreas();
	});

	var getAreas = function (object) {
		var department = $('#inputDepartment').val();
		$.get('/areas/?department='+department)
		.then(function (data) {
			$('#inputArea').find("option[value!='']").remove();    	
	    	for(var i in data) {
	    		var department = data[i];
	    		var option = '<option value="'+department['id']+'">'+department['name']+'</option>';
	    		$('#inputArea').append(option);
	    	}
	    	$('#inputArea').selectpicker('refresh');
		})
		.then(function () {
			if (object) setFormValues(object);				
		});
	}

	var reloadPage = function (data) {
		$(location).attr('href', '/employees/')
	}	
});