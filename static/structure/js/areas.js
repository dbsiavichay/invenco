$(function () {
	$('.selectpicker').selectpicker();

	var areaId;
	var areaDepartmentField = $('#selDepartment');
	var areaCodeField = $('#txtCode');
	var areaNameField = $('#txtName');

	$('.glyphicon-plus-sign').parent().on('click', function () {				
		openAreaModel()
	});

	$('.glyphicon-pencil').parent().on('click', function () {
		areaId = $(this).parent().attr('id');
		$.get('/areas/'+areaId, function (area) {						
			openAreaModel(area);
		});
	});

	$('.glyphicon-remove').parent().on('click', function () {
		areaId = $(this).parent().attr('id');		
		$('#objectDeleteModal').modal('show');
	});


	$('#btnSave').on('click', function () {		
		var data = getData();
		if (data) makeRequest('/areas/', 'POST', data);
	});

	$('#btnEdit').on('click', function () {		
		var data = getData();		
		if (data) makeRequest('/areas/'+data.id+'/', 'POST', data);
	});

	$('#btnDelete').on('click', function () {
		makeRequest('/areas/'+areaId+'/', 'DELETE', {});
	});


	var getData = function () {
		var id = parseInt(areaId);
		var department = areaDepartmentField.val();
		var code = areaCodeField.val();
		var name = areaNameField.val();
		var is_valid = true;

		cleanErrorForm()

		if (!department) {			
			areaDepartmentField.parents('.form-group').addClass('has-error');
			is_valid = false;
		} 

		if (!code) {			
			areaCodeField.parents('.form-group').addClass('has-error');
			is_valid = false;
		} 

		if (!name) {
			areaNameField.parents('.form-group').addClass('has-error');
			is_valid = false;
		}

		if (is_valid) {
			var data = {
				id: id,				
				code: code,
				name: name,
				department: department
			}
			return data;			
		}
	}


	var openAreaModel = function (area) {
		cleanErrorForm()

		if (area) {
			areaDepartmentField.selectpicker('val', area.department);
			areaCodeField.val(area.code);
			areaNameField.val(area.name);
			$('#btnEdit').show();
			$('#btnSave').hide();
		} else {
			areaDepartmentField.selectpicker('val', '');
			areaCodeField.val('')
			areaNameField.val('');
			$('#btnEdit').hide();
			$('#btnSave').show();
		}		
		$('#objectModal').modal('show');
	}

	var cleanErrorForm = function () {
		var departmentFormGroup = areaDepartmentField.parents('.form-group');
		var codeFormGroup = areaCodeField.parents('.form-group');
		var nameFormGroup = areaNameField.parents('.form-group');
		if (departmentFormGroup.hasClass('has-error')) departmentFormGroup.removeClass('has-error');
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
	    	$(location).attr('href', '/areas/');
	    });

	    request.error(function (error) {
	    	console.log(error);
	    });
	}		
});