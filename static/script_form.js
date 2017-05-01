
// function getHTMLString is creating a lengthy string by concatenating string array (builds HTML dynamically) which is used 
// to create dynamic form 

function getHTMLString(formCount) {
    var complex_html = [
              '<div class="form-inline">',
                '<select class="input-small form-control" id="primitive-selector'+ formCount +'" name="PrimitiveChoose[]">',
                  '<option value="sphere">sphere</option>',
                  '<option value="triangle">triangle</option>',
                '</select> ',
                '<input type="number" class="input-small form-control" id="diameter'+ formCount +'"  name="Diameter[]" step="any" placeholder="diameter(D)"> ',
                '<input type="text" class="form-control"  id="sphere-position'+ formCount +'" name="SpherePosition[]"  placeholder="(x, y, z)"> ',
                '<input type="text" class="A form-control" id="A-position'+ formCount +'" name="VerticeAPosition[]" placeholder="(x, y, z)"> ',
              	'<input type="text" class="B form-control" id="B-position'+ formCount +'" name="VerticeBPosition[]" placeholder="(x, y, z)"> ',
              	'<input type="text" class="C form-control" id="C-position'+ formCount +'" name="VerticeCPosition[]" placeholder="(x, y, z)"> ',
  
              	'<select class="input-small form-control" id="material-selector'+ formCount +'" name="MaterialSelect[]">',
		        '<option value=" " disabled="" selected="">material</option>',
		        '<option value="normal">opaque</option>',
		        '<option value="glass">glass</option>',
		        '<option value="mirror">mirror</option>',
		        '</select> ',

                '<select class="input-small form-control" id="circle-color-selector'+ formCount +'" name="CircColorSelect[]">',
                  '<option value=" " disabled selected>color</option>',
                  '<option value="red">red</option>',
                  '<option value="blue">blue</option>',
                  '<option value="green">green</option>',
                  '<option value="yellow">yellow</option>',    
                '</select> ', 
                '<button type="button" class="btn btn-success btn-add" id="remove_more'+ formCount +'"> <span class="glyphicon glyphicon-minus" aria-hidden="true"></span>',
                '</button>',  
            '</div>',
    ].join('');
    return complex_html;

}

	var formCount = 0;  // global variable formCount

	/* This jQuery click event handler removes the dynamically added forms for primitives in the scene of Ray Tracer. 
	Attach a click event to the <document> element where Jquery attribute start with selector is used, 
	"[id^=remove_more]" (specified attribute begining exactly with a given string [name^='value']). This selector is useful for 
	identifying elements produced by server-side frameworks where HTML produced with systematic element IDs. */ 

	$(document).on("click", "[id^=remove_more]", function(e){ 
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
	    var TselectorString = '#A-position'+ formCount + ', #B-position'+ formCount +
	            ', #C-position'+ formCount;
	    var SselectorString = '#diameter'+ formCount + ', #sphere-position'+ formCount +
	            ', #material-selector'+ formCount + ', #circle-color-selector'+ formCount
	    var IsS = $(this).val() === "sphere";
	    $(SselectorString).toggle(IsS);
	    $(TselectorString).toggle(!IsS);
	});

	/* When the Document Object Model ($(document)) is ready for JavaScript code to execute, a jQuery click event handler is 
	implemented to add a multiple field form using the helper function getHTMLString(formCount).  */
	$(document).ready(function() {
		console.log("here")
	    $('#add_more').on('click', function(e) {
	    	e.preventDefault();  
	        if (formCount < 4) {
	            var html = getHTMLString(formCount);
	         	$('#dynamic_form  .form-group').append(html);
	         	var TselectorString = '#A-position'+ formCount + ', #B-position'+ formCount +
	            ', #C-position'+ formCount;
			    var SselectorString = '#diameter'+ formCount + ', #sphere-position'+ formCount +
			            ', #material-selector'+ formCount + ', #circle-color-selector'+ formCount
			    
				$(SselectorString).toggle(true);
			    $(TselectorString).toggle(false);
	        } else {
	            return;
	        }
	        formCount++;
	    });

	    /* This jQuery event handler using jQuery.getJSON() in order to Load JSON-encoded data from the server using a GET HTTP request. */

	    $('#the-form').on('submit', function() {
	    	
	    	/* jQuery.getJSON(URL, [data], [callback])
	    	url: A string containing the URL to which the request sent
	    	data: optional parameter which represents key/value pairs that will be sent to the server
	    	callback: optional parameter represents a function to be executed whenever the data is loaded successfully */
			
	  		$.getJSON('/result', {
	    		light_position: $('[id="light-position"]').val(),
	    		image_size: $('[id="image-size-selector"]').val(),
	    		ambient_illumination: $('[id="ambient-illumination"]').val()
	    				
	   		}, function(data) {
	   	 			$('#image').html('<img src="data:image/png;base64,' + data.data + '" />');
	   			});
	   			return false;
	  	});
	});


