$(document).ready(graphSocket);

var graph_namespace = '/graph';
var ping_pong_times = [];
var graph_active = true;
var start_time;
var read_count;
var socket;

function pageInit(){
    $('#colFFTGraph').hide();
    $('form#formCreateGraph').submit(formCreateGraph_submit);
    $('form#formDisconnect').submit(formDisconnect_submit);
    $('#formSaveSettings *').filter(':input').change(formSaveSettings_change);
    $('#rngFreqRange').change(rngFreqRange_change);
    $('#rngFreqRange').on('input', rngFreqRange_input);
    $('#inpDevIndex').keypress(inputKeyPress);
    $('#inpSampRate').keypress(inputKeyPress);
    $('#inpCenterFreq').keypress(inputKeyPress);
    $('#inpNumRead').keypress(inputKeyPress);
    $('#inpInterval').keypress(inputKeyPress);
    $('#rngFreqRange').attr('step', Math.pow(10, 6)/5); 
}
function formCreateGraph_submit(event){
    if (graph_active){
        socket.emit('start_sdr');
    }else{
        socket.emit('stop_sdr');
    }
    return false;
}
function formDisconnect_submit(event){
    socket.emit('disconnect_request');
    on_log_message("Disconnecting...")
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
function rngFreqRange_change(){
    socket.emit('restart_sdr', $('#rngFreqRange').val());
}
function rngFreqRange_input(){
    $('#spnFreqRange').text(parseFloat(parseInt($('#rngFreqRange').val())/Math.pow(10, 6)))
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

    socket.on('dev_status', function(status) {
        if(parseInt(status) == 0){
            $('#formSaveSettings :input').prop('disabled', false);
            $('#formDisconnect :input').prop('disabled', false);
            graph_active = true;
            $('#btnCreateGraph').val("Create FFT graph");            
        }else if(parseInt(status) == 1) {
            $('#formSaveSettings :input').prop('disabled', true);
            $('#formDisconnect :input').prop('disabled', true);
            graph_active = false;
            $('#btnCreateGraph').val("Stop");
            read_count = 0;
            $('#rngFreqRange').attr('max', parseInt($('#inpCenterFreq').val())+20*(Math.pow(10, 6)));
            $('#rngFreqRange').attr('min', parseInt($('#inpCenterFreq').val())-20*(Math.pow(10, 6)));
            $('#rngFreqRange').val(parseInt($('#inpCenterFreq').val()));
            $('#spnFreqRange').text(parseFloat(parseInt($('#rngFreqRange').val())/Math.pow(10, 6)))
        }
    });

    socket.on('new_freq_set', function(status) {
        $('#inpCenterFreq').val($('#rngFreqRange').val())
        socket.emit('start_sdr', $('#rngFreqRange').val());
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
