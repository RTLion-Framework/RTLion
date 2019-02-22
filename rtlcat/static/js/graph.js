$(document).ready(graphSocket);

var graph_namespace = '/graph';
var create_graph = true;
var ping_pong_times = [];
var start_time;
var read_count;
var socket;

function pageInit(){
    $('#colFFTGraph').hide();
    $('form#formCreateGraph').submit(formCreateGraph_submit);
    $('form#formDisconnect').submit(formDisconnect_submit);
    $('#formSaveSettings *').filter(':input').change(formSaveSettings_change);
    $('#inpDevIndex').keypress(inputKeyPress);
    $('#inpSampRate').keypress(inputKeyPress);
    $('#inpCenterFreq').keypress(inputKeyPress);
    $('#inpNumRead').keypress(inputKeyPress);
    $('#inpInterval').keypress(inputKeyPress);
}
function formCreateGraph_submit(event){
    if (create_graph){
        create_graph = false;
        $('#btnCreateGraph').val("Stop");
        read_count = 0;
        socket.emit('start_sdr');
    }else{
        create_graph = true;
        $('#btnCreateGraph').val("Create FFT graph");
        socket.emit('stop_sdr');
    }
    return false;
}
function formDisconnect_submit(event){
    socket.emit('disconnect_request');
    $('#divLog').append('Disconnecting...<br>');
    $('#divLog').scrollTop($('#divLog').height());
    setTimeout(function() {
        location.reload();
    }, 2000);
    return false;
}
function formSaveSettings_change(){
    args = {
        'dev': parseInt($('#inpDevIndex').val()), 
        'samprate': parseInt($('#inpSampRate').val()), 
        'gain': $('#inpDevGain').val(), 
        'freq': parseInt($('#inpCenterFreq').val()),
        'n': parseInt($('#inpNumRead').val()),
        'i': parseInt($('#inpInterval').val())
    };
    if(checkArgs(args)){
        socket.emit('update_settings', args);
    }else{
        socket.emit('send_cli_args');
    }
}
function inputKeyPress(evt){
    var charCode = (evt.which) ? evt.which : event.keyCode
    if (charCode > 31 && (charCode < 48 || charCode > 57))
        return false;
    return true;
}
function checkArgs(args){
    if (args['dev'] < 0 || args['dev'] > 20 || args['samprate'] < 0 ||
     args['gain'] < 0 || args['freq'] <= 0 || args['freq'] == "" || 
     isNaN(args['freq']) || args['freq'] == null || args['i'] < 0 || args['n'] < -1){
        on_log_message("Invalid settings detected.");
        $('#spnSettingsLog').text('Invalid settings detected.');
        setTimeout(function() {
            $('#spnSettingsLog').text('');
        }, 1000);
        $('#btnCreateGraph').prop("disabled", true);
        return false;
    }
    $('#btnCreateGraph').prop("disabled", false);
    return true;
}
function on_log_message(msg){
    current_time = new Date().toLocaleTimeString().split(' ')[0];
    $('#divLog').append("<b>[" + current_time + "]</b> " + msg + "<br>");
    $('#divLog').scrollTop($('#divLog').height());
}
function graphSocket() {
    pageInit();
    socket = io.connect(location.protocol + '//' + document.domain + 
                 ':' + location.port + graph_namespace);

    socket.on('connect', function() {
        socket.emit('send_cli_args');
    });

    socket.on('log_message', function(log) {
        on_log_message(log.msg);   
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
        for (var i in args){
            if (i != 'freq')
                args[i] = args[i] || 0;
        }
        checkArgs(args);
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
