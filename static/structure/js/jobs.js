$(function () {
	var job_name = $('#txtName');
	$('.glyphicon-plus-sign').parent().on('click', function () {
		job_name.val('');
		$('#btnEdit').hide();
		$('#btnSave').show();
		$('#jobModal').modal('show');
	});

	$('.glyphicon-pencil').parent().on('click', function (event) {
		event.preventDefault();
		$('#btnEdit').show();
		$('#btnSave').hide();
		var id = $(this).parent().attr('id');
		$.get('/jobs/'+id, function (data) {
			var job = JSON.parse(data);
			job_name.val(job.name);
			$('#jobModal').modal('show');
		});
	});
});