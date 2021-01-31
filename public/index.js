
$('#main-div2').fadeOut('fast');
var fun1 = function () {
	document.getElementById('label').innerHTML = "";
	// alert("abcd");
	$('#btn').prop('disabled', 'true');
	$('#main-div').fadeOut(700);

	setTimeout(function () {
		$('#main-div2').fadeIn('slow');
	}, 800);
	setTimeout(function () {
		$('#main-div2').fadeOut(700);
	}, 10800);
	setTimeout(function () {
		$('#main-div3').fadeIn('slow');
	}, 11550);

	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function () {
		if (this.readyState == 4 && this.status == 200) {
			$('#btn').removeAttr('disabled');
			setTimeout(function () {
				$('#main-div3').fadeOut(700);
			}, 0);
			setTimeout(function () {
				$('#main-div').fadeIn('slow');
			}, 800);
			document.getElementById('label').innerHTML = xhttp.responseText;

		}
	};
	xhttp.open("GET", "http://127.0.0.1:6789/detect", true);
	xhttp.send();

}

const realtime = (id) => {
	setTimeout(function () {
		document.getElementById('realtime-btn').innerHTML = 'Start Recording Audio';
	}, 10000)
	document.getElementById('realtime-btn').innerHTML = 'Recording Audio .....'
	document.getElementById('realtime-btn').setAttribute('class', 'btn btn-danger mt-5')

	var video = document.getElementById('video-div');
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function () {
		if (this.readyState == 4 && this.status == 200) {
			document.getElementById('responseText').innerHTML = xhttp.responseText;
			document.getElementById('realtime-btn').setAttribute('class', 'btn btn-success mt-5')


			console.log(xhttp.responseText);
			video.setAttribute('src', 'final_clip.mp4');
			video.load();
			video.play();
		}
	};
	xhttp.open("GET", "http://127.0.0.1:6789/detect", true);
	xhttp.send();
}
