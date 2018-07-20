
$(document).ready(function(){

	$('#the-form').on('submit', function(e) {
    	e.preventDefault();
    	// reset progress bar after rendering an image and sending progress report
    	var elem = document.getElementById("progress");
    	elem.style.width = 0
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

		flask_sent_all_data_dict["sid"] = window.socket.id;
		
		// $.ajax({
		// 	type: 'POST',
		// 	url: '/result',
		// 	data: JSON.stringify(flask_sent_all_data_dict),
		// 	dataType: 'json',
		// 	contentType: 'application/json; charset=utf-8',
		// 	success: function (msg) {
		// 		console.log(msg);
		// 		if (msg.status !== 200) {
		// 			alert(msg.message);
		// 		}
		// 	},
		// 	failure: function (errMsg) {
		// 		console.log(errMsg);
		// 	}

		// });

		window.socket.emit('submit_data', flask_sent_all_data_dict);


		return false;
	});


	document.getElementById("example1").addEventListener("click", function example1(){
		var flask_sent_all_data_dict = {};
		flask_sent_all_data_dict["imageSize"] = 256;
		flask_sent_all_data_dict["lightPosition"] = "(2, 6.5, -2)";
		flask_sent_all_data_dict["ambIllumination"] = 0.11;
		flask_sent_all_data_dict["dynamicForm"] = [{'sphere':{'color': 'red', 'material':'mirror', 'radius':'2', 'sphere-position':'(4, 2, 5)'}}];
		$('#image-size-selector').val(256);
		$('#light-position').val('(2, 6.5, -2)');
		$('#ambient-illumination').val(0.11);
		$('#radius0').val('2');
		$('#sphere-position0').val('(4, 2, 5)');
		$('#color0').val('(255, 91, 91)');
		$('#material-selector0').val('mirror');
		window.socket.emit('submit_data', flask_sent_all_data_dict);
	});
});

// window.testFunction = testFunction;


