$(document).ready(mainPage);

var index_namespace = '/';
var anim_speed = 600;
var socket;

function fadeInAnim(){
    $("#imgLogo").delay(50).animate({"opacity": "1"}, anim_speed);
    $("#spnDesc").delay(500).animate({"opacity": "1"}, anim_speed);
    $("#divFWActions").delay(800).animate({"opacity": "1"}, anim_speed);
    $("#btnGithub").delay(1000).animate({"opacity": "1"}, anim_speed);
    $("#btnInfo").delay(1000).animate({"opacity": "1"}, anim_speed);
}
function pageInit(){
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