$(document).ready(mainPage);

function fadeInAnim(){
    $("#imgLogo").delay(50).animate({"opacity": "1"}, 700);
    $("#spnDesc").delay(500).animate({"opacity": "1"}, 700);
    $("#divFFTGraphArea").delay(800).animate({"opacity": "1"}, 700);
}
function pageInit(){
    fadeInAnim();
    $("#btnFFTGraph").click(btnFFTGraph_click);
}
function btnFFTGraph_click(){
    window.location.replace("/graph");
}
function mainPage() {
    pageInit();
    namespace = '/';
    var socket = io.connect(location.protocol + '//' + document.domain + 
                 ':' + location.port + namespace);

    socket.on('connect', function() {
        //
    });
}