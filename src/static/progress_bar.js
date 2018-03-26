
$(document).ready(function() {
	/* sending percentage data from celery worker to the front end(progress bar) through socketio */
	/* so the progress function checks if the counter is equal to data.data(percentage). If not it updates
	the width of the "progress" element in HTML. Then rquestAnimationFrame() calls for progress and counter will be added by
	one. This process continues till counter === data.data and stop updating the progress bar and waits for the next data.data(percentage) 
	from backend.
	requestAnimationFrame() is used because it waits until the browser is ready to update the page, so it will be smoother.
	Also, requestAnimatinFrame() is asynchronous, so the app can still be used while the progress bar is loading.
	 */
	
	namespace = '/result';
	// define socket
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

	window.socket = socket; // window is a global object and we put socket as a variable in the global object

	socket.on('send_prog_perc', function(data){
		var elem = document.getElementById("progress");
		var counter = data.data-25;
		function progress(){
			if (counter != data.data){
				elem.style.width = counter*3 + 'px'; // counter is multiplied by 3 in order to increase the width of progress bar to 300 px instead of 100 px
				requestAnimationFrame(progress);
				counter += 1;
			}
		}
		progress();
    });

	// URI data of the image is sent to the front end through socketio
    socket.on('send_image', function(data) {

	// to set image source with base 64, setAttribute has been used.
    	document.getElementById('primitives-image').setAttribute('src', 'data:image/png;base64,'+ data.data);
    	document.getElementById('glyphicon-modal-trigger').style.visibility = 'visible';

    	// passing image_size to CSS for max-width
		var imageSize = $('#image-size-selector').val();
		if (imageSize == 1024){
			$('#primitives-image').css({ "width": 512});
			$('#image-wrapper').css({ "width": 512});
			$('#image-wrapper').css({ "height": 512});
		} else {
			$('#primitives-image').css({ "width": imageSize});
			$('#image-wrapper').css({ "width": imageSize});
			$('#image-wrapper').css({ "height": imageSize});	
		}
		$('modalImage').css({"width": imageSize});
		$('modalImage').css({"height": imageSize});
    });
});

