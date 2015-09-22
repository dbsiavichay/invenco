$(function () {
	var name = $('#txtName');
	$('.glyphicon-plus-sign').parent().on('click', function () {
		name.val('');
		$('#jobModal').modal('show');
	});

	$('.glyphicon-pencil').parent().on('click', function (event) {
		event.preventDefault();
		var row = $(this).parents('tr');
		var nombre = $(row.children().get(0)).html();
		name.val(nombre);
		$('#jobModal').modal('show');
	});
});