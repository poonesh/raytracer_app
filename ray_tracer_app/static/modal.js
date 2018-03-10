
$(document).ready(function() {
	// Get the modal
	var modal = document.getElementById('myModal');

	// Get the image and insert it inside the modal - use its "alt" text as a caption
	var modalTrigger = document.getElementById('glyphicon-modal-trigger');
	var modalImg = document.getElementById("modalImage");
	var captionText = document.getElementById("caption");
	var imgSrc = document.getElementById("primitives-image");
	modalTrigger.onclick = function(){
	    modal.style.display = "block";
	    modalImg.src = imgSrc.src;
	    // hide the navbar
	    document.getElementById('navbar').style.display = 'none';    
	};

	// Get the <span> element that closes the modal
	var span = document.getElementsByClassName("close")[0];

	// When the user clicks on <span> (x), close the modal
	span.onclick = function() { 
	  modal.style.display = 'none';
	  document.getElementById('navbar').style.display = 'initial'; 
	};
});