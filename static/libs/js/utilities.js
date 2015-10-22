var makeRequest = function (url, method, data, callback) {
	var request = $.ajax({
        url: url,        
        method: method, 
        data: data,
        dataType: 'json'	        
    });

    request.then(callback);

    request.error(function (error) {
    	console.log(error);
    });
}

var getData = function (container) {
	var data = {};
	var fields = container?container.find('[id*=input]'):$('[id*=input]');

	fields.each(function (index, field) {
		var type = 	$(field).attr('type');
		var name = $(field).attr('name');		
		//var value = type!='radio'?$(field).val():$(field).find('input:checked').val();
		var value = type==='radio'?$(field).find('input:checked').val():type==='checkbox'?$(field).prop('checked'):$(field).val();
		data[name] = value;		
	});

	return data;	
}

var cleanFormErrors = function () {
	var fields = $('[id*=input]');

	fields.each(function (index, field) {
		var form_group = $(field).parents('.form-group');
		if(form_group.hasClass('has-error')) form_group.removeClass('has-error');		
	});	
}

var resetFormValues = function () {	
	var fields = $('[id*=input]');

	fields.each(function (index, field) {
		var type = 	$(field).attr('type');
		if(type==='radio') {
			var first_radio = $(field).find('input').get(0);
			$(first_radio).prop('checked', true);
		}else if (type === 'checkbox') {
			$(field).prop('checked', true);
		}else if (type === 'select'){
			$(field).selectpicker('val', '');
		}else{
			$(field).val('');
		}
	});	
}

var setFormValues = function (object) {	
	var fields = $('[id*=input]');
	fields.each(function (index, field) {
		var type = $(field).attr('type');
		var name = $(field).attr('name');	
		if(type==='radio') {
			var radio = $(field).find("input[value='"+object[name]+"']");
			$(radio).prop('checked', true);
		}else if (type === 'checkbox') {
			$(field).prop('checked', object[name]);
		}else if (type === 'select'){
			$(field).selectpicker('val', object[name]);
		}else if (type === 'date'){
			var matches = object[name].match(/\d{4}-\d{1,2}-\d{1,2}/);
			if (matches) $(field).val(matches[0]);			
		}else{
			$(field).val(object[name]);
		}
	});
}

var validateForm = function () {
	var fields = $('[id*=input]');
	var is_valid = true;

	cleanFormErrors();
	fields.each(function (index, field) {
		var type = $(field).attr('type');
		var is_required = $(field).attr('req');
		if(type!='radio' && is_required) {
			var value = $(field).val().trim();
			if(!value) {
				$(field).parents('.form-group').addClass('has-error');
				is_valid = false;
			}
		}
	});	

	return is_valid;
}

var openModal = function (object) {
	cleanFormErrors();
	if(!object) {
		resetFormValues();
		$('#btnEdit').hide();
		$('#btnSave').show();		
	} else {
		setFormValues(object)
		$('#btnEdit').show();
		$('#btnSave').hide();
	}

	$('#objectModal').modal('show');	
}

