
// function getHTMLString is creating a lengthy string by concatenating string array (builds HTML dynamically) which is used 
// to create dynamic form 

function getHTMLString(formCount) {
    var complex_html = [
              '<div class="form-inline">',
                '<select class="input-small form-control" id="primitive-selector'+ formCount +'" name="PrimitiveChoose[]">',
                  '<option value="sphere">sphere</option>',
                  '<option value="triangle">triangle</option>',
                '</select> ',
                '<input type="text" class="input-small form-control" id="radius'+ formCount +'"  name="Radius[]" step="any" placeholder="radius(r)" size="7"> ',
                '<input type="text" class="form-control"  id="sphere-position'+ formCount +'" name="SpherePosition[]"  placeholder="position(x, y, z)" size="13"> ',
                '<input type="text" class="A form-control" id="A-position'+ formCount +'" name="VerticeAPosition[]" placeholder="vertex(x, y, z)" size="13"> ',
              	'<input type="text" class="B form-control" id="B-position'+ formCount +'" name="VerticeBPosition[]" placeholder="vertex(x, y, z)" size="13"> ',
              	'<input type="text" class="C form-control" id="C-position'+ formCount +'" name="VerticeCPosition[]" placeholder="vertex(x, y, z)" size="13"> ',
                '<input type="text" class="Sphere form-control" id="color'+ formCount +'" name="ColorSelect[]" placeholder="color(255, 255, 255)" size="17"> ',
		        '<select class="input-small form-control" id="material-selector'+ formCount +'" name="MaterialSelect[]"> ',
                '<option value=" " disabled="" selected="">material</option>',
                '<option value="normal">opaque</option>',
                '<option value="glass">glass</option>',
                '<option value="mirror">mirror</option>',
              	'</select> ',
                '<button type="button" class="btn btn-success btn-add" id="remove_more'+ formCount +'"> <span class="glyphicon glyphicon-minus" aria-hidden="true"></span>',
                '</button>',  
            '</div>',
    ].join('');
    return complex_html;

}

/* This function returns an object with all the properties of Triangle primitives 
chosen by the user. The returned object will be appended to an array called dynamicFoem 
in the following. This array will be the value for key "dynamicForm" in the final object called 
finalDic */

function createTriangleParameter(i, dict){
	var new_dict = {}
	var triangle_dict = {}
	for (var key in dict){
		if (key[key.length-1] == i){
			if (key === "#A-position"+i){
				new_dict["vertexA"] = dict[key];	
			} else if (key === "#B-position"+i){
				new_dict["vertexB"] = dict[key];
			} else if (key === "#C-position"+i){
				new_dict["vertexC"] = dict[key];
			} else if (key === "#color"+i){
				new_dict["color"] = dict[key];
			} else if (key === "#material-selector"+i){
				new_dict["material"] = dict[key];
			}			
		}
	}
	triangle_dict["triangle"] = new_dict;
	return triangle_dict;
}

/* This function returns an object with all the properties of Sphere primitives 
chosen by the user. The returned object will be appended to an array called dynamicFoem 
in the following. This array will be the value for key "dynamicForm" in the final object called 
finalDic */

function createSphereParameter(i, dict){
	var new_dict = {}
	var sphere_dict = {}
	for (var key in dict){
		if (key[key.length-1] == i){
			if (key === "#radius"+i){
				new_dict["radius"] = dict[key];	
			} else if (key === "#sphere-position"+i){
				new_dict["sphere-position"] = dict[key];
			} else if (key === "#color"+i){
				new_dict["color"] = dict[key];
			} else if (key === "#material-selector"+i){
				new_dict["material"] = dict[key];
			}			 
		}
	}
	sphere_dict["sphere"] = new_dict;
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
	    // console.log('here I am!')
	    // console.log(this.id)
	    var formCount = this.id.replace('primitive-selector', '');
	    console.log(formCount)
	    var TselectorString = '#A-position'+ formCount + ', #B-position'+ formCount + ', #C-position'+ formCount; 
	    var SselectorString = '#radius'+ formCount + ', #sphere-position'+ formCount;

	    console.log(TselectorString);
	    console.log(SselectorString);

	    var IsS = $(this).val() === "sphere";
	    $(TselectorString).toggle(!IsS);
	    $(SselectorString).toggle(IsS);
	});

	/* When the Document Object Model ($(document)) is ready for JavaScript code to execute, a jQuery click event handler is 
	implemented to add a multiple field form using the helper function getHTMLString(formCount).  */
	$(document).ready(function() {
		namespace = '/result';
		var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
		
		
		console.log("here")
	    $('#add_more').on('click', function(e) {
	    	e.preventDefault(); 
	    	console.log("addHere") 
	        if (formCount < 5) {
	            var html = getHTMLString(formCount);
	         	$('#dynamic_form .form-group').append(html);

	         	var TselectorString = '#A-position'+ formCount + ', #B-position'+ formCount + ', #C-position'+ formCount; 
	    		var SselectorString = '#radius'+ formCount + ', #sphere-position'+ formCount;
			    
				$(TselectorString).toggle(false);
			    $(SselectorString).toggle(true);
	        } else {
	            return;
	        }
	        formCount++;
	    });

	    /* This jQuery event handler creates the final object (finalDic) which will be sent to Flask.*/ 
	    $('#the-form').on('submit', function(e) {
	    	e.preventDefault();
	     	var dict = {};
	 	/* querySelectorAll returns all the children of ('div.form-inline > *'). Then creates an object with the ids and values
	 	of all the children */  
			var children = document.querySelectorAll('div.form-inline > *');
			for (var i=0; i<children.length; i++){
				var id = children[i].id;
				id = "#" + id;
				var value = $(id).val();
				dict[id] = value;
			}

		/* appending the sphere and triangle properties to dynamicForm */	
			var dynamicForm = []
			for (var i=0; i<5; i++){
				type = dict['#primitive-selector'+ i];
				if (type === "sphere") {
					var final_dict = createSphereParameter(i, dict);
					dynamicForm[i] = final_dict;	 
				} else if (type === "triangle") {
					var final_dict = createTriangleParameter(i, dict);
					dynamicForm[i] = final_dict;
				}
			}
		/* final object to be sent to flask using Ajax */	
			var finalDic = {};
			finalDic["imageSize"] = $('#image-size-selector').val();
			finalDic["dynamicForm"] = dynamicForm;
			finalDic["lightPosition"] = $('#light-position').val();
			finalDic["ambIllumination"] = $('#ambient-illumination').val();

			$.ajax({
				type: 'POST',
				url: '/result',
				data: JSON.stringify(finalDic),
				dataType: 'json',
				contentType: 'application/json; charset=utf-8',
				success: function (result) {
        			console.log(result);
    			},
    			failure: function (errMsg) {
        			console.log(errMsg);
    			}

			});
			return false;

	  	});

		/* sending percentage data from celery worker to the front end */
		/* progress bar */
				
		socket.on('send_prog_perc', function(data) {
			console.log(data.data);
			var elem = document.getElementById("progress");
			var counter = data.data-25;
			function progress(){
				if (counter != data.data){
					elem.style.width = counter*3 + 'px';
					requestAnimationFrame(progress);
					counter += 1;
				}
			}
			progress();
        });


        socket.on('send_image', function(data) {
        	document.getElementById('primitives-image').setAttribute( 'src', 'data:image/png;base64,'+ data.data);

        });

	});

function testFunction(){
		console.log("inside testFunction!")
    	var finalDic = {};
    	finalDic["imageSize"] = 256;
    	finalDic["lightPosition"] = "(2, 6.5, -2)";
    	finalDic["ambIllumination"] = 0.11;
    	finalDic["dynamicForm"] = [{'sphere':{'color':'(255, 0, 0)', 'material':'normal', 'radius':'1', 'sphere-position':'(4, 4, -6)'}}]

    	$.ajax({
			type: 'POST',
			url: '/result',
			data: JSON.stringify(finalDic),
			dataType: 'json',
			contentType: 'application/json; charset=utf-8',
			success: function (result) {
        		console.log(result);
    		},
    		failure: function (errMsg) {
        		console.log(errMsg);
    		},
    		error: function (errMsg) {
        		console.log(errMsg);
    		}

		});
		return false;

    }


 