$(function () { 
	var trademarkId;
	var trademarkNameField = $('#txtName');

	$('.glyphicon-plus-sign').parent().on('click', function () {				
		openTrademarkModal()
	});

	$('.glyphicon-pencil').parent().on('click', function () {
		trademarkId = $(this).parent().attr('id');
		$.get('/trademarks/'+trademarkId, function (trademark) {						
			openTrademarkModal(trademark);
		});
	});

	$('.glyphicon-remove').parent().on('click', function () {
		trademarkId = $(this).parent().attr('id');		
		$('#objectDeleteModal').modal('show');
	});


	$('#btnSave').on('click', function () {		
		var data = getData();
		if (data) makeRequest('/trademarks/', 'POST', data);
	});

	$('#btnEdit').on('click', function () {		
		var data = getData();		
		if (data) makeRequest('/trademarks/'+data.id+'/', 'POST', data);
	});

	$('#btnDelete').on('click', function () {
		makeRequest('/trademarks/'+trademarkId+'/', 'DELETE', {});
	});


	var getData = function () {
		var id = parseInt(trademarkId);
		var name = trademarkNameField.val();
		if (name) {
			var data = {
				id: id,
				name: name
			}
			return data;			
		} else {
			trademarkNameField.parents('.form-group').addClass('has-error');
		}
	}

	var openTrademarkModal = function (trademark) {
		var formGroup = $('#txtName').parents('.form-group');		
		if (formGroup.hasClass('has-error')) formGroup.removeClass('has-error');
		if (trademark) {
			trademarkNameField.val(trademark.name);
			$('#btnEdit').show();
			$('#btnSave').hide();
		}
		else {
			trademarkNameField.val('');
			$('#btnEdit').hide();
			$('#btnSave').show();
		}		
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
	    	$(location).attr('href', '/trademarks/');
	    });

	    request.error(function (error) {
	    	console.log(error);
	    });
	}		
});