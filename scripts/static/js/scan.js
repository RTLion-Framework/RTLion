$(document).ready(scannerSocket);

var scan_namespace = '/scan';
var ping_pong_times = [];
var start_time;
var socket;

function scannerSocket(){
    socket = io.connect(location.protocol + '//' + document.domain + 
                 ':' + location.port + scan_namespace);
    socket.on('connect', function() {
        socket.emit('send_cli_args');
    });

    socket.on('server_pong', function() {
        var latency = (new Date).getTime() - start_time;
        ping_pong_times.push(latency);
        ping_pong_times = ping_pong_times.slice(-30);11
        var sum = 0;
        for (var i = 0; i < ping_pong_times.length; i++)
            sum += ping_pong_times[i];
        $('#spnPingPong').text(Math.round(10 * sum / ping_pong_times.length) / 10 + "ms");
    });
    
    window.setInterval(function() {
        start_time = (new Date).getTime();
        socket.emit('server_ping');
    }, 1000);
}