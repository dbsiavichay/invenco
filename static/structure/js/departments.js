$(function () { 
	var departmentId;
	var departmentCodeField = $('#txtCode');
	var departmentNameField = $('#txtName');

	$('.glyphicon-plus-sign').parent().on('click', function () {				
		openDepartmentModal()
	});

	$('.glyphicon-pencil').parent().on('click', function () {
		departmentId = $(this).parent().attr('id');
		$.get('/departments/'+departmentId, function (department) {						
			openDepartmentModal(department);
		});
	});

	$('.glyphicon-remove').parent().on('click', function () {
		departmentId = $(this).parent().attr('id');		
		$('#objectDeleteModal').modal('show');
	});


	$('#btnSave').on('click', function () {		
		var data = getData();
		if (data) makeRequest('/departments/', 'POST', data);
	});

	$('#btnEdit').on('click', function () {		
		var data = getData();		
		if (data) makeRequest('/departments/'+data.id+'/', 'POST', data);
	});

	$('#btnDelete').on('click', function () {
		makeRequest('/departments/'+departmentId+'/', 'DELETE', {});
	});


	var getData = function () {
		var id = parseInt(departmentId);
		var code = departmentCodeField.val();
		var name = departmentNameField.val();
		var is_valid = true;

		cleanErrorForm()

		if (!code) {			
			departmentCodeField.parents('.form-group').addClass('has-error');
			is_valid = false;
		} 

		if (!name) {
			departmentNameField.parents('.form-group').addClass('has-error');
			is_valid = false;
		}

		if (is_valid) {
			var data = {
				id: id,
				code: code,
				name: name
			}
			return data;			
		}
	}


	var openDepartmentModal = function (department) {
		cleanErrorForm()

		if (department) {
			departmentCodeField.val(department.code);
			departmentNameField.val(department.name);
			$('#btnEdit').show();
			$('#btnSave').hide();
		} else {
			departmentCodeField.val('')
			departmentNameField.val('');
			$('#btnEdit').hide();
			$('#btnSave').show();
		}		
		$('#objectModal').modal('show');
	}

	var cleanErrorForm = function () {
		var codeFormGroup = departmentCodeField.parents('.form-group');
		var nameFormGroup = departmentNameField.parents('.form-group');
		if (codeFormGroup.hasClass('has-error')) codeFormGroup.removeClass('has-error');
		if (nameFormGroup.hasClass('has-error')) nameFormGroup.removeClass('has-error');
	}


	var makeRequest = function (url, method, data) {
		var request = $.ajax({
	        url: url,        
	        method: method, 
	        data: data,
	        dataType: 'json'	        
	    });

	    request.done(function (data) {	    		    	
	    	$(location).attr('href', '/departments/');
	    });

	    request.error(function (error) {
	    	console.log(error);
	    });
	}		
});