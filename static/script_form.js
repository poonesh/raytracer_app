
$(document).ready(function() {
	
	$('#the-form').on('submit', function() {
		console.log("hello")
	  $.getJSON('/result', {
	    x: $('input[id="Point-Light-X"]').val(),
	    y: $('input[id="Point-Light-Y"]').val(),
	    z: $('input[id="Point-Light-Z"]').val()
	   }, function(data) {
	   	 $('#image').html('<img src="data:image/png;base64,' + data.data + '" />');
	   });
	   return false;
	  });

});