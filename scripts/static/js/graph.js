$(document).ready(graphSocket);

var graphNamespace = '/graph';
var pingPongTimes = [];
var graphActive = true;
var startTime;
var readCount;
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
    if (graphActive){
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
    var args = {
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
    $('#spnFreqRange').text(parseFloat(parseInt($('#rngFreqRange').val())/Math.pow(10, 6)));
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
    var currentTime = new Date().toLocaleTimeString().split(' ')[0];
    $('#divLog').append("<b>[" + currentTime + "]</b> " + msg + "<br>");
    $('#divLog').scrollTop($('#divLog').height());
}
function graphSocket() {
    pageInit();
    socket = io.connect(location.protocol + '//' + document.domain + 
                 ':' + location.port + graphNamespace);

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
            graphActive = true;
            $('#btnCreateGraph').val("Create FFT graph");            
        }else if(parseInt(status) == 1) {
            $('#formSaveSettings :input').prop('disabled', true);
            $('#formDisconnect :input').prop('disabled', true);
            graphActive = false;
            $('#btnCreateGraph').val("Stop");
            readCount = 0;
            $('#rngFreqRange').attr('max', parseInt($('#inpCenterFreq').val())+20*(Math.pow(10, 6)));
            $('#rngFreqRange').attr('min', parseInt($('#inpCenterFreq').val())-20*(Math.pow(10, 6)));
            $('#rngFreqRange').val(parseInt($('#inpCenterFreq').val()));
            $('#spnFreqRange').text(parseFloat(parseInt($('#rngFreqRange').val())/Math.pow(10, 6)));
        }
    });

    socket.on('new_freq_set', function(status) {
        $('#inpCenterFreq').val($('#rngFreqRange').val());
        socket.emit('start_sdr', $('#rngFreqRange').val());
    });

    socket.on('fft_data', function(msg) {
        $('#imgFFTGraph').attr("src", "data:image/png;base64," + msg.data);
        readCount++;
        if($('#inpNumRead').val() == "-1"){
            $('#spnReads').text('(' + readCount + '/∞)');
        }else{
            var percentage = parseInt((readCount * 100) / parseInt($('#inpNumRead').val()));
            $('#spnReads').text('('+ readCount+ '/' + $('#inpNumRead').val() + ') [%' + percentage + "]");
            if(readCount == parseInt($('#inpNumRead').val()))
                $('#btnCreateGraph').click();
        }
        if(!$('#colFFTGraph').is(':visible')){
            $('#colFFTGraph').show();
        }
    });

    socket.on('cli_args', function(cliargs) {
        var args = cliargs.args;
        for (var i in args){
            if (i != 'freq')
                args[i] = args[i] || 0;
        }
        checkArgs(args);
        $("#inpDevIndex").val(args.dev);
        $("#inpSampRate").val(args.samprate);
        $("#inpDevGain").val(args.gain);
        $("#inpCenterFreq").val(args.freq);
        $("#inpNumRead").val(args.n);
        $("#inpInterval").val(args.i);
        readCount = args.n;
        if (cliargs.status == 1){
            $('#spnSettingsLog').text('Settings saved.');
            setTimeout(function() {
                $('#spnSettingsLog').text('');
            }, 1000);
        }
    });

    socket.on('server_pong', function() {
        var latency = (new Date).getTime() - startTime;
        pingPongTimes.push(latency);
        pingPongTimes = pingPongTimes.slice(-30);
        var sum = 0;
        for (var i = 0; i < pingPongTimes.length; i++)
            sum += pingPongTimes[i];
        $('#spnPingPong').text(Math.round(10 * sum / pingPongTimes.length) / 10 + "ms");
    });
    
    window.setInterval(function() {
        startTime = (new Date).getTime();
        socket.emit('server_ping');
    }, 1000);
}
