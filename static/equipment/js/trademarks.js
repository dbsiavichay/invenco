$(function () {
	var id;
	addEventListenerOnNew();
	addEventListenerOnEdit();
	addEventListenerOnRemove();
	addEventListenerOnCreate();
	addEventListenerOnUpdate();
	addEventListenerOnDelete();
});

var getUrl = function () {
	return '/trademarks/'
}

var addEventListenerOnNew = function () {
	$('.glyphicon-plus-sign').parent().on('click', function () {
		openModal()
	});
}

var addEventListenerOnEdit = function () {
	$('.glyphicon-pencil').parent().on('click', function () {
		id = $(this).parent().attr('id');
		$.get(getUrl()+id+'/', function (object) {
			openModal({'object':object});
		});
	});
}

var addEventListenerOnRemove = function () {
	$('.glyphicon-remove').parent().on('click', function () {
		id = $(this).parent().attr('id');
		$('#objectDeleteModal').modal('show');
	});
}

var addEventListenerOnCreate = function () {
	$('#btnSave').on('click', function () {
		var is_valid = validateForm();
		if(!is_valid) return;
		makeRequest(getUrl(), 'POST', getData(), reloadPage);
	});
}

var addEventListenerOnUpdate = function () {
	$('#btnEdit').on('click', function () {
		var is_valid = validateForm();
		if(!is_valid) return;
		makeRequest(getUrl()+id+'/', 'POST', getData(), reloadPage);
	});
}

var addEventListenerOnDelete = function () {
	$('#btnDelete').on('click', function () {
		makeRequest(getUrl()+id+'/', 'DELETE', {}, reloadPage);
	});
}

var reloadPage = function (data) {
	$(location).attr('href', getUrl());
}

//Funcionalidad para busquedas
var getRow = function (object) {
	var $row = $rowTemplate.clone();
	for (var attr in object) {
		if(attr=='id') {
			$row.find('[name=actions]').attr('id', object[attr])
		}else{
			$row.find('[name="'+attr+'"]').text(object[attr]);
		}
	}
	return $row;
}
