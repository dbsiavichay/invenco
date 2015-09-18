$(function () {
	var name = $('#txtName');
	$('.glyphicon-plus-sign').parent().on('click', function () {
		name.val('');
		$('#departmentModal').modal('show');
	});
});