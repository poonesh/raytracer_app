
$(document).ready(function(){
	$('#the-form').on('submit', function(e) {
    	e.preventDefault();
    	console.log(8);
     	var id_value_dict = {};
	 	/* querySelectorAll returns all the children of ('div.form-inline > *'). Then creates an object(dictionary) with the keys(unique_ids) and 
	 	values(values filled by the user) of all the children */  
		var children = document.querySelectorAll('div.form-inline > *');
		for (var index=0; index<children.length; index++){			
			var id = children[index].id;
			id = '#' + id;
			if (id === "#"){
				continue;
			};
			var value = $(id).val();
			id_value_dict[id] = value;
		}
		console.log(9);
		/* appending the sphere(flask_sent_sphere_dict) and triangle(flask_sent_triangle_dict) properties to dynamicForm_values */	
		var dynamicForm_values = [];
		for (var index=0; index<5; index++){
			type = id_value_dict['#primitive-selector'+ index];
			if (type === "sphere") {
				var flask_sent_sphere_dict = createSphereParameter(index, id_value_dict);
				dynamicForm_values[index] = flask_sent_sphere_dict;	 
			} else if (type === "triangle") {
				var flask_sent_triangle_dict = createTriangleParameter(index, id_value_dict);
				dynamicForm_values[index] = flask_sent_triangle_dict;
			}
		}
		/* flask_sent_all_data_dict object(dictionary) to be sent to flask using Ajax */
		var flask_sent_all_data_dict = {};
		flask_sent_all_data_dict["imageSize"] = $('#image-size-selector').val();
		flask_sent_all_data_dict["dynamicForm"] = dynamicForm_values; // the value of this key is an array of input data by the user
		flask_sent_all_data_dict["lightPosition"] = $('#light-position').val();
		flask_sent_all_data_dict["ambIllumination"] = $('#ambient-illumination').val();
		
		$.ajax({
			type: 'POST',
			url: '/result',
			data: JSON.stringify(flask_sent_all_data_dict),
			dataType: 'json',
			contentType: 'application/json; charset=utf-8',
			success: function (msg) {
				console.log(msg);
				if (msg.status !== 200) {
					alert(msg.message);
				}
			},
			failure: function (errMsg) {
				console.log(errMsg);
			}

		});
		return false;
	});
});

