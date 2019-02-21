$(document).ready(graphSocket);

var graph_namespace = '/graph';
var create_graph = true;
var ping_pong_times = [];
var start_time;
var read_count;
var socket;

function pageInit(){
    $('#colFFTGraph').hide();
}

function graphSocket() {
    pageInit();
    socket = io.connect(location.protocol + '//' + document.domain + 
                 ':' + location.port + graph_namespace);

    socket.on('connect', function() {
        socket.emit('send_cli_args');
    });

    socket.on('client_message', function(msg) {
        $('#divLog').append(msg.data + '<br>');
        $('#divLog').scrollTop($('#divLog').height());
    });
    socket.on('fft_data', function(msg) {
        $('#imgFFTGraph').attr("src", "data:image/png;base64," + msg.data);
        read_count++;
        if($('#inpNumRead').val() == "-1"){
            $('#spnReads').text('(' + read_count + '/∞)');
        }else{
            $('#spnReads').text('('+ read_count+ '/' + $('#inpNumRead').val() + ')');
        }
        if(!$('#colFFTGraph').is(':visible')){
            $('#colFFTGraph').show();
        }
    });
    socket.on('cli_args', function(cliargs) {
        args = cliargs.args;
        $("#inpDevIndex").val(args.dev);
        $("#inpSampRate").val(args.samprate);
        $("#inpDevGain").val(args.gain);
        $("#inpCenterFreq").val(args.freq);
        $("#inpNumRead").val(args.n)
        $("#inpInterval").val(args.i);
        read_count = args.n;
        if (cliargs.status == 1){
            $('#spnSettingsLog').text('Settings saved.');
            setTimeout(function() {
                $('#spnSettingsLog').text('');
            }, 1000);
        }
    });
    window.setInterval(function() {
        start_time = (new Date).getTime();
        socket.emit('server_ping');
    }, 1000);
    socket.on('server_pong', function() {
        var latency = (new Date).getTime() - start_time;
        ping_pong_times.push(latency);
        ping_pong_times = ping_pong_times.slice(-30);11
        var sum = 0;
        for (var i = 0; i < ping_pong_times.length; i++)
            sum += ping_pong_times[i];
        $('#spnPingPongs').text(Math.round(10 * sum / ping_pong_times.length) / 10 + "ms");
    });

    $('form#formCreateGraph').submit(function(event) {
        if (create_graph){
            // Check arguments
            create_graph = false;
            $('#btnCreateGraph').val("Stop");
            read_count = 0;
            socket.emit('create_fft_graph');
        }else{
            create_graph = true;
            $('#btnCreateGraph').val("Create FFT graph");
            socket.emit('stop_sdr');
        }
        return false;
    });
    $('#formSaveSettings *').filter(':input').change(function() {
        // Check arguments here
        socket.emit('update_settings',
        {'dev': parseInt($('#inpDevIndex').val()), 
        'samprate': parseInt($('#inpSampRate').val()), 
        'gain': $('#inpDevGain').val(), 
        'freq': parseInt($('#inpCenterFreq').val()),
        'n': parseInt($('#inpNumRead').val()),
        'i': parseInt($('#inpInterval').val())});
    });
}
