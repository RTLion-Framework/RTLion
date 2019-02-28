$(document).ready(mainPage);

function fadeInAnim(){
    $("#imgLogo").delay(50).animate({"opacity": "1"}, 700);
    $("#spnDesc").delay(500).animate({"opacity": "1"}, 700);
    $("#divFFTGraphArea").delay(800).animate({"opacity": "1"}, 700);
}
function mainPage() {
    fadeInAnim();
    $("#btnFFTGraph").click(function () {
        window.location.replace("/graph"); 
    });
    namespace = '/';
    var socket = io.connect(location.protocol + '//' + document.domain + 
                 ':' + location.port + namespace);

    socket.on('connect', function() {
        //
    });
}