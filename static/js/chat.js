$(document).ready(function() {
    $("#input").keypress(function(event) {
	if (event.which == 13) {
	    event.preventDefault();
	    send();
	}
    });
});

function setInput(text) {
    $("#input").val(text);
    send();
}

function send() {
    var text = $("#input").val();
    $.ajax({
	type: "POST",
	url: '/chat/',
	data: { input : text },
	success: function(data) {
	    setResponse(JSON.stringify(data.botOutput));
	},
	error: function() {
	    setResponse("Internal Server Error");
	}
    });
    setResponse("Loading...");
}
function setResponse(val) {
    $("#response").text(val);
}
