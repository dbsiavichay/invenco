var getDataByType = function(type) {
	var url = '/dispatch/add/?type=' + type;
	return $.get(url);
}

var showModal = function () {
	$('#myModal').modal('show');
}

var hideModal = function () {
	$('#myModal').modal('hide');
}

/////////////
var openModal = function (event) {	
	var self = this;
	var $target = $(event.target);
	var type = $target.attr('pk');

	if (!$target.is('a')) type = $target.parents('a').attr('pk');

	getDataByType(type)
	.then(function (response) {
		self.models = response['data'];		
	})
	.then(function () {
		$('.select2').select2();
		$('#quantity').val('');
		showModal();
	});	
}

var submit = function (event) {
	var self = this;
	var data = $('#frm-modal').serializeArray().reduce(function (obj, item) {		    	
     	obj[item.name] = item.value;
     	return obj;
    }, {});

	for(var i in self.models) {
		var model = self.models[i];
		if (model.id == data.model) {
			self.dispatches.push({
				id: model.id,
				product: model.type + ' ' + model.model,
				quantity: data.quantity,
				properties: model.properties
			});
			hideModal();
			break;
		}
	}
}

var app = new Vue({
	el: '#app',
	data: {
	    models: [],
	    dispatches: []
	},
	methods:{
	  	openModal:openModal,
	  	submit:submit,
	}
});




// $(function () {
// 	var currentResponse;

// 	var $validator = $('#frm-modal').validate({
// 		submitHandler: function(form) {			
// 		    var dataList = getDataForTable(form, currentResponse);
// 		    renderTable('#tb-dispatch', [dataList]);
// 		    closeModal();
// 		}
// 	});

// 	$('.launch-modal').on('click', function (e) {
// 		e.preventDefault();

// 		type = $(this).attr('pk');

// 		$.get('/dispatch/add/?type=' + type, function (response) {
// 			currentResponse = response;

// 			var data = getDataForSelect(currentResponse)
// 			renderSelect('.select-model', data);			
// 			openModal();
// 		});

// 	});
// });

// var openModal = function () {
// 	$('#quantity').val('');
// 	$('#myModal').modal('show');
// }

// var closeModal = function () {
// 	$('#myModal').modal('hide');
// }

// var getDataForSelect = function (response) {
// 	data = [];

// 	for (var i in response) {
// 		obj = response[i];
// 		data.push({
// 			id: obj['id'],
// 			text: obj['type'] + ' ' + obj['model'] + '|' + obj['stock'],
// 		});
// 	}

// 	return data;
// }

// var getDataForTable = function (form, response) {	
//     var dataList = []
//     var data = $(form).serializeArray().reduce(function (obj, item) {		    	
//     	obj[item.name] = item.value;
//     	return obj;
//     }, {});

//     for (var i in response) {
//     	var item = response[i];
//     	if (parseInt(item.id) === parseInt(data.model)) {
//     		dataList.push(item.type + ' ' + item.model);
//     		dataList.push(data.quantity);
//     		dataList.push(item.properties);
//     		break;
//     	}
//     }

//     return dataList
// }

// var renderSelect = function (select, data) {
// 	var $select = $(select);
// 	$select.children().remove();
// 	$select.select2({
// 		data:data,
// 	})

// 	$select.on('change', function (data) {
// 		console.log(data);
// 	});
// }


// var renderTable = function (table, dataList) {	

// 	var templateRow = '<tr></tr>';
// 	var templateColumn = '<td></td>';
// 	var templateActions =   '<td class="col-xs-3">' +					        	
// 					        	'<a href="/brand/{{ brand.id }}/edit/" class="btn btn-default btn-xs">'+
// 					        		'<span class="fa fa-pencil"></span>'+
// 					        	'</a>'+
// 					        	'<button class="btn btn-default btn-xs delete" data-model="brand" data-id="{{ brand.id }}">'+
// 					        		'<span class="fa fa-trash"></span>'+
// 					        	'</button>'+
// 					        '</td>'

// 	var templateList = '<ul></ul>';
// 	var templateListItem = '<li></li>';

// 	$body = $(table).find('tbody');
// 	$body.find('.empty-row').remove();

// 	for (var i in dataList) {
// 		list = dataList[i]
// 		var $row = $(templateRow).clone();
// 		for (var j in list) {
// 			var item = list[j];
// 			var $column = $(templateColumn).clone();

// 			if ($.isArray(item)) item = getHtmlList(item)

// 			$column.append(item);
// 			$row.append($column);
// 		}
// 		$actions = $(templateActions).clone();
// 		$row.append($actions);
// 		$body.append($row);
// 	}
// }

// var getHtmlList = function (data) {
// 	var templateList = '<ul></ul>';
// 	var templateListItem = '<li></li>';

// 	var list = $(templateList).clone();

// 	for (var i in data) {
// 		var item = data[i];
// 		var listItem = $(templateListItem).clone();

// 		listItem.append(item);
// 		list.append(listItem);
// 	}

// 	return list;
// }