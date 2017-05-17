$(function () {
	var type;

	$('.delete').on('click', function () {
		var model = $(this).attr('data-model');
		var pk = $(this).attr('data-id');
		var url = '/' + model + '/' + pk + '/delete/' 
		$('#delete').attr('action', url);
		$('#delete-modal').modal('show');		
	});	




	//Select type
	$('.type-item').on('click', function () {
		var next = $('#next').text();

		var type = $(this).attr('type-id');
		var set = $(this).attr('set-id');

		var url;
		if (type) url = '/'+ next +'/add/type/' + type + '/';
		else if (set) url = '/'+ next +'/add/set/' + set + '/';
					
		$('#selectTypeNext').attr('href', url);
		$('.type-item').removeClass('active');
		$(this).addClass('active');
	});

	//Code for assignments
	$('#id_area').on('change', function () {
		var codes = $('#id_area').val().split(':');
		$('input[name=department]').val(codes[0]);
		$('input[name=section]').val(codes[1]);
	});
});