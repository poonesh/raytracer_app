
// function getHTMLString is creating a lengthy string by concatenating string array (builds HTML dynamically) which is used 
// to create dynamic form 

function getHTMLString(formCount) {
    var complex_html = [
              '<div class="form-inline" id="primitive-form">',
                '<select class="primitive-selector input-small form-control" id="primitive-selector'+ formCount +'" name="PrimitiveChoose'+ formCount +'">',
                  '<option value="sphere">sphere</option>',
                  '<option value="triangle">triangle</option>',
                '</select> ',
                '<input type="text" class="radius input-small form-control" id="radius'+ formCount +'"  name="Radius'+ formCount +'" step="any" placeholder="radius(r)" size="7"> ',
                '<input type="text" class="sphere-position form-control"  id="sphere-position'+ formCount +'" name="SpherePosition'+ formCount +'"  placeholder="position(x, y, z)" size="13"> ',
                '<input type="text" class="vertex-A form-control" id="A-position'+ formCount +'" name="VerticeAPosition'+ formCount +'" placeholder="vertex(x, y, z)" size="13"> ',
              	'<input type="text" class="vertex-B form-control" id="B-position'+ formCount +'" name="VerticeBPosition'+ formCount +'" placeholder="vertex(x, y, z)" size="13"> ',
              	'<input type="text" class="vertex-C form-control" id="C-position'+ formCount +'" name="VerticeCPosition'+ formCount +'" placeholder="vertex(x, y, z)" size="13"> ',
                '<input type="text" class="sphere-color form-control" id="color'+ formCount +'" name="ColorSelect'+ formCount +'" placeholder="color(255, 255, 255)" size="17"> ',
		        '<select class="material-selector input-small form-control" id="material-selector'+ formCount +'" name="MaterialSelect'+ formCount +'"> ',
	                '<option value=" " disabled="" selected="">material</option>',
	                '<option value="normal">opaque</option>',
	                '<option value="glass">glass</option>',
	                '<option value="mirror">mirror</option>',
              	'</select> ',
                '<button type="button" class="btn btn-success btn-add" id="remove_more'+ formCount +'"> <span class="glyphicon glyphicon-minus" aria-hidden="true"></span>',
                '</button>',
                '<div id="dynamic-form-error"></div>',  
            '</div>',
    ].join('');
    return complex_html;
}

/* This function takes two parameters, id_value_dict(which is a dictionary with unique ids of the fields for triangle primitive as the keys and the 
values that the user fills for the fields) and index which is a value between 0 to 4 corresponding to a unique index for each primitive and its fields 
in the dynamic form). This function returns an object(dictionary) with all the properties of a specific Triangle(Triangle0,....., Triangle4) 
chosen by the user. The returned object will be appended to an array called dynamicForm 
in the following. This array will be the value for key "dynamicForm_value" in the final object called 
flask_sent_all_data_dict */

function createTriangleParameter(index, id_value_dict){
	var temp_dict = {};
	var triangle_dict = {};
	for (var key in id_value_dict){
		if (key[key.length-1] == index){
			if (key === "#A-position"+index){
				temp_dict["vertexA"] = id_value_dict[key];	
			} else if (key === "#B-position"+index){
				temp_dict["vertexB"] = id_value_dict[key];
			} else if (key === "#C-position"+index){
				temp_dict["vertexC"] = id_value_dict[key];
			} else if (key === "#color"+index){
				temp_dict["color"] = id_value_dict[key];
			} else if (key === "#material-selector"+index){
				temp_dict["material"] = id_value_dict[key];
			}			
		}
	}
	triangle_dict["triangle"] = temp_dict;
	return triangle_dict;
}

/* This function takes two parameters, dict(which is a dictionary with unique ids of the fields for sphere primitive as the keys and the 
values that the user fills for the fields) and index which is a value between 0 to 4 corresponding to a unique index for each primitive and its fields 
in the dynamic form). This function returns an object(dictionary) with all the properties of a specific Triangle(Triangle0,....., Triangle4) 
chosen by the user. The returned object will be appended to an array called dynamicForm 
in the following. This array will be the value for key "dynamicForm_value" in the final object called 
flask_sent_all_data_dict */

function createSphereParameter(index, id_value_dict){
	var temp_dict= {};
	var sphere_dict = {};
	for (var key in id_value_dict){
		if (key[key.length-1] == index){
			console.log("create_sphere_parameter",key[key.length-1])
			if (key === "#radius"+index){
				temp_dict["radius"] = id_value_dict[key];	
			} else if (key === "#sphere-position"+index){
				temp_dict["sphere-position"] = id_value_dict[key];
			} else if (key === "#color"+index){
				temp_dict["color"] = id_value_dict[key];
			} else if (key === "#material-selector"+index){
				temp_dict["material"] = id_value_dict[key];
			}			 
		}
	}
	sphere_dict["sphere"] = temp_dict;
	return sphere_dict;
}
	
var formCount = 1;  // global variable formCount

/* This jQuery click event handler removes the dynamically added forms for primitives in the scene of Ray Tracer. 
Attach a click event to the <document> element where Jquery attribute start with selector is used, 
"[id^=remove_more]" (specified attribute begining exactly with a given string [name^='value']). This selector is useful for 
identifying elements produced by server-side frameworks where HTML produced with systematic element IDs. */ 

$(document).on('click', '[id^=remove_more]', function(e){ 
    e.preventDefault(); // stops the default behaviour of an HTML element

// 'this' is the DOM element which triggers the event. This line (closest()) returns the first form-inline 
// of the DOM element ('this') and remove it. (which starts with the current element here). 
    $(this).closest('div.form-inline').remove(); 
    formCount--;
});


/* This jQuery change event handler display the fields of the dynamic form based on the choosen primitive by the user.
If the choosen primitive is Sphere the .toggle() method shows $(SselectorString) otherwise shows $(TselectorString). */ 
$(document).on('change', '[id^=primitive-selector]', function() {
// 'this' here is DOM (HTML) element  and this.id.replace('primitive-selector', '') basically 
// returns the numeric part of id (which is produced here by server side)
    var formCount = this.id.replace('primitive-selector', '');
    var TselectorString = '#A-position'+ formCount + ', #B-position'+ formCount + ', #C-position'+ formCount; 
    var SselectorString = '#radius'+ formCount + ', #sphere-position'+ formCount;
    var IsS = $(this).val() === "sphere";
    $(TselectorString).toggle(!IsS);
    $(SselectorString).toggle(IsS);
});


// function testFunction(){
// 	var flask_sent_all_data_dict = {};
// 	flask_sent_all_data_dict["imageSize"] = 128;
// 	flask_sent_all_data_dict["lightPosition"] = "(2, 6.5, -2)";
// 	flask_sent_all_data_dict["ambIllumination"] = 0.11;
// 	flask_sent_all_data_dict["dynamicForm"] = [{'sphere':{'color':'(255, 0, 0)', 'material':'mirror', 'radius':'1', 'sphere-position':'(4, 4, -6)'}}];

// 	$.ajax({
// 		type: 'POST',
// 		url: '/result',
// 		data: JSON.stringify(flask_sent_all_data_dict),
// 		dataType: 'json',
// 		contentType: 'application/json; charset=utf-8',
// 		success: function (msg) {
//     		console.log(msg);
// 		},
// 		failure: function (errMsg) {
//     		console.log(errMsg);
// 		},
// 		error: function (errMsg) {
//     		console.log(errMsg);
// 		}

// 	});


// 	return false;

// }


