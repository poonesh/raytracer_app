
$(document).ready(function() {
	$.validator.addMethod(
        "regex",
        function(value) {
            var coordinates = value.substring(1, value.length-1);
            var numbers = coordinates.split(',');
            if (numbers.length != 3){
            	return false;
            }
            for (var i=0; i<numbers.length; i++){
            	if(!isNaN(Number.parseFloat(numbers[i]))){
					valid = true;
            	}else{
            		valid = false;
            		return valid;
            	}
        	}
        	return valid;
		}, 

		"the input should be a format of (0, 0, 0)"
	);
	
	$('#the-form').validate({
		rules:{
			Radius: {
				required: true
			},
			SpherePosition:{
				required: true,	regex: true
			},
			VerticeAPosition:{
				required: true, regex: true
			},
			VerticeBPosition:{
				required: true, regex: true
			},
			VerticeCPosition:{
				required: true, regex: true
			},
			LightPosition:{
				required: true, regex: true
			}

		},
			messages:{
			Radius:{
				required: "Radius field is required."
			},
			SpherePosition:{
				required: "Sphere position is required."
			},
			VerticeAPosition:{
				required: "Vertex position is required."
			},
			VerticeBPosition:{
				required: "Vertex position is required."
			},
			VerticeCPosition:{
				required: "Vertex position is required."
			},
			SpherePositon:{
				required: "Vertex position is required."
			},
			LightPosition:{
				required: "Light position is required."
			}	
		},
		
		// highlight: function (element) {
  //           $(element).parent().addClass('error');
  //       },
  //       unhighlight: function (element) {
  //           $(element).parent().removeClass('error');
  //       },
		errorLabelContainer: "#validation_error",
		wrapper:'li',
		submitHandler: function(form, e) {
			e.preventDefault();
	     	var id_value_dict = {};
		 	/* querySelectorAll returns all the children of ('div.form-inline > *'). Then creates an object(dictionary) with the keys(unique_ids) and 
		 	values(values filled by the user) of all the children */  
			var children = document.querySelectorAll('div.form-inline > *');
			for (var index=0; index<children.length; index++){
				var id = children[index].id;
				id = "#" + id;
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
		}
	});
	/* When the Document Object Model ($(document)) is ready for JavaScript code to execute, a jQuery click event handler is 
	implemented to add a multiple field form using the helper function getHTMLString(formCount).  */
	$('#add_more').on('click', function(e) {
    	e.preventDefault();
        if (formCount < 5) {
            var html = getHTMLString(formCount);
         	$('#dynamic_form .form-group').append(html);
         	// validate the form using jQuery validation plugin
         	$('input.vertex-A').each(function(){
				$(this).rules('add', {
					required: true, 
					regex: true,
					messages:{
						required: "vertex-A is required."
					}
				});
			});
         	console.log("checking if you are here too!");
			$('input.vertex-B').each(function(){
				$(this).rules('add', {
					required: true, 
					regex: true,
					messages:{
						required: "vertex-B is required."
					}
				});
			});

			$('input.vertex-C').each(function(){
				$(this).rules('add', {
					required: true, 
					regex: true,
					messages:{
						required: "vertex-C is required."
					}
				});
			});

			$('select.sphere-color').each(function(){
				$(this).rules('add', {
					required: true,
					messages:{
						required: "Color is required."
					}
				});
			});
			
			$('select.material-selector').each(function(){
				$(this).rules('add', {
					required: true,
					messages:{
						required: "Material is required."
					}
				});
			});

			$('input.sphere-position').each(function(){
				$(this).rules('add', {
					required: true, 
					regex: true,
					messages:{
						required: "Sphere position is required."
					}
				});
			});

			$('input.radius').each(function(){
				$(this).rules('add', {
					required: true,
					messages:{ 
						required: "Radius field is required."
				    }	
				});
			});
         	var TselectorString = '#A-position'+ formCount + ', #B-position'+ formCount + ', #C-position'+ formCount; 
    		var SselectorString = '#radius'+ formCount + ', #sphere-position'+ formCount;
			$(TselectorString).toggle(false);
		    $(SselectorString).toggle(true);
        }else{
            return;
        }
        formCount++;
    });
});

