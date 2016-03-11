var $rowTemplate = $($('#objectList tr')[0]).clone();

$(function () {
	$('#search').focus();

	$('#loadSearchs').on('click', function (event) {
		event.preventDefault();
		search();
	});

	$('#search').on('keyup', function (event) {
		if(event.keyCode != 13) return;
		$('.load-searchs').removeAttr('next-page');
		search();
	});

});

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
			value = $(field).attr('default')?true:false;
			$(field).prop('checked', value);
		}else if (type === 'select'){
			$(field).selectpicker('val', '');
		}else{
			$(field).val('');
		}
	});
}

var setFormValues = function (object) {
	for(name in object) {
		var $field = $('[id*=input][name="'+name+'"]');
		var type = $field.attr('type');
		if(type==='radio') {
			var radio = $field.find("input[value='"+object[name]+"']");
			$(radio).prop('checked', true);
		}else if (type === 'checkbox') {
			$field.prop('checked', object[name]);
		}else if (type === 'select'){
			$field.selectpicker('val', object[name]);
		}else if (type === 'date'){
			var matches = object[name].match(/\d{4}-\d{1,2}-\d{1,2}/);
			if (matches) $field.val(matches[0]);
		}else{
			$field.val(object[name]);
		}
	}
}

/*var setFormValues = function (object) {
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
}*/

var validateForm = function (form) {
	var fields = form?$(form).find('[id*=input]'):$('[id*=input]');
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

var openModal = function (options) {
	var options = options || {};

	cleanFormErrors();
	if(!options['object']) {
		resetFormValues();
		$('#btnEdit').hide();
		$('#btnSave').show();
	} else {
		setFormValues(options['object'])
		$('#btnEdit').show();
		$('#btnSave').hide();
	}

	var tabs = $('#objectModal').find('.nav-tabs').find('a');

	if(tabs) {
		if (options['tabs']) {
			tabs.hide();
			for(var i in options['tabs']) {
				var index = options['tabs'][i]
				$(tabs[index-1]).show();
			}
			$(tabs[options['tabs'][0]-1]).tab('show');
		}else{
			tabs.show();
			$(tabs[0]).tab('show');
		}
	}

	$('#objectModal').modal('show');
}

//Funcionalidad para busquedas
var renderTable = function (data, page) {
	var $table = $('#objectList');
	if (!page) $table.children().remove();
	for (var i = 0; i < data.length - 1; i++) {
		var object = data[i];
		$table.append(getRow(object));
	}
	addEventListenerOnEdit();
	addEventListenerOnRemove();
	if (data[data.length - 1].has_next) {
		$('.load-searchs').show();
		$('.load-searchs').attr('next-page', data[data.length - 1].next_page_number)
	} else {
		$('.load-searchs').hide();
	}
}

var hidePagination = function () {
	var $pagination = $('.section-pagination');
	if ($pagination.is(':visible')) $pagination.hide();
}

var search = function () {
	var page = $('.load-searchs').attr('next-page');
	var keyword = $('#search').val();
	var url = getUrl() + '?keyword=' + keyword;
	if (!keyword) reloadPage();
	if (page) url = url + '&page='+ page;
	hidePagination();
	$.get(url)
	.then(function (data) {
		renderTable(data, page);
	})
	.fail(function (error) {
		console.log(error)
	});
}
