$(document).ready(scannerSocket);

var scan_namespace = '/scan';
var ping_pong_times = [];
var start_time;
var socket;

function scannerSocket(){
    socket = io.connect(location.protocol + '//' + document.domain + 
                 ':' + location.port + scan_namespace);
}