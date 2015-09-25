$(function () { 
	var jobId;
	var jobNameField = $('#txtName');

	$('.glyphicon-plus-sign').parent().on('click', function () {				
		openJobModal()
	});

	$('.glyphicon-pencil').parent().on('click', function () {
		jobId = $(this).parent().attr('id');
		$.get('/jobs/'+jobId, function (job) {						
			openJobModal(job);
		});
	});

	$('.glyphicon-remove').parent().on('click', function () {
		jobId = $(this).parent().attr('id');		
		$('#objectDeleteModal').modal('show');
	});


	$('#btnSave').on('click', function () {		
		var data = getData();
		if (data) makeRequest('/jobs/', 'POST', data);
	});

	$('#btnEdit').on('click', function () {		
		var data = getData();		
		if (data) makeRequest('/jobs/'+data.id+'/', 'POST', data);
	});

	$('#btnDelete').on('click', function () {
		makeRequest('/jobs/'+jobId+'/', 'DELETE', {});
	});


	var getData = function () {
		var id = parseInt(jobId);
		var name = jobNameField.val();
		if (name) {
			var data = {
				id: id,
				name: name
			}
			return data;			
		} else {
			jobNameField.parents('.form-group').addClass('has-error');
		}
	}

	var openJobModal = function (job) {
		var formGroup = $('#txtName').parents('.form-group');		
		if (formGroup.hasClass('has-error')) formGroup.removeClass('has-error');
		if (job) {
			jobNameField.val(job.name);
			$('#btnEdit').show();
			$('#btnSave').hide();
		}
		else {
			jobNameField.val('');
			$('#btnEdit').hide();
			$('#btnSave').show();
		}
		$('#successAlert').hide();
		$('#objectModal').modal('show');
	}


	var makeRequest = function (url, method, data) {
		var request = $.ajax({
	        url: url,        
	        method: method, 
	        data: data,
	        dataType: 'json'	        
	    });

	    request.done(function (data) {	    		    	
	    	$(location).attr('href', '/jobs/');
	    });

	    request.error(function (error) {
	    	console.log(error);
	    });
	}		
});