$(document).ready(mainPage);

var index_namespace = '/';
var socket;

function fadeInAnim(){
    $("#imgLogo").delay(50).animate({"opacity": "1"}, 700);
    $("#spnDesc").delay(500).animate({"opacity": "1"}, 700);
    $("#divFFTGraphArea").delay(800).animate({"opacity": "1"}, 700);
    $("#spnDevStatus").delay(800).animate({"opacity": "1"}, 700);
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
    socket = io.connect(location.protocol + '//' + document.domain + 
                 ':' + location.port + index_namespace);
    socket.on('connect', function() {
        //
    });
}