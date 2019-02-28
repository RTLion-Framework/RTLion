$(document).ready(mainPage);

var index_namespace = '/';
var socket;

function fadeInAnim(){
    $("#imgLogo").delay(50).animate({"opacity": "1"}, 700);
    $("#spnDesc").delay(500).animate({"opacity": "1"}, 700);
    $("#divFWActions").delay(800).animate({"opacity": "1"}, 700);
}
function pageInit(){
    fadeInAnim();
    $("#btnFFTGraph").click(btnFFTGraph_click);
    $("#btnExitFW").click(btnExitFW_click);
}
function btnFFTGraph_click(){
    window.location.replace("/graph");
}
function btnExitFW_click(){
    socket.emit('disconnect_request');
    setTimeout(function() {
        location.reload();
    }, 2000);
}
function mainPage() {
    pageInit();
    socket = io.connect(location.protocol + '//' + document.domain + 
                 ':' + location.port + index_namespace);

    socket.on('connect', function() {
        socket.emit('get_dev_status');
    });
    
    socket.on('dev_status', function(status) {
        if(parseInt(status) == 0){
            $("#spnDevStatus").text("[!] No RTL-SDR device found.");
        }else if(parseInt(status) == 1) {
            $("#spnDevStatus").text("[+] RTL-SDR device found.");
        }
        $("#spnDevStatus").delay(800).animate({"opacity": "1"}, 700);
    });
}