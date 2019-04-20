$(document).ready(documentReady);

var indexNamespace = '/';
var animSpeed = 600;
var socket;

function fadeInAnim(){
    $("#imgLogo").delay(50).animate({"opacity": "1"}, animSpeed);
    $("#spnDesc").delay(500).animate({"opacity": "1"}, animSpeed);
    $("#divFWActions").delay(800).animate({"opacity": "1"}, animSpeed);
    $("#btnGithub").delay(1000).animate({"opacity": "1"}, animSpeed);
    $("#btnInfo").delay(1000).animate({"opacity": "1"}, animSpeed);
}
function initializePage(){
    fadeInAnim();
    $("#btnFFTGraph").click(btnFFTGraph_click);
    $("#btnFreqScan").click(btnFreqScan_click);
    $("#btnAndroidApp").click(btnAndroidApp_click);
    $("#btnExitFW").click(btnExitFW_click);
}
function btnFFTGraph_click(){
    window.location.replace("/graph");
}
function btnFreqScan_click(){
    window.location.replace("/scan");
}
function btnAndroidApp_click(){
    window.location.replace("/app");
}
function btnExitFW_click(){
    socket.emit('disconnect_request');
    setTimeout(function() {
        location.reload();
    }, 2000);
}
function documentReady() {
    initializePage();
    socket = io.connect(location.protocol + '//' + document.domain + 
                 ':' + location.port + indexNamespace);

    socket.on('connect', function() {
        socket.emit('get_dev_status');
    });
    
    socket.on('dev_status', function(status) {
        if(parseInt(status) == 1)
            $("#spnDevStatus").text("[+] RTL-SDR device found.");
        else
            $("#spnDevStatus").text("[!] No RTL-SDR device found.");
        $("#spnDevStatus").delay(800).animate({"opacity": "1"}, 700);
    });
}