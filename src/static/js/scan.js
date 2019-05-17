$(document).ready(documentReady);

var scanNamespace = '/graph';
var pingPongTimes = [];
var graphActive = true;
var startTime;
var numRead;
var centerFreq;
var interval;
var currentFreq;
var minFreq;
var maxFreq;
var freqRes = [];
var dbRes = [];
var stepSize;
var currentRead;
var maxRead;
var socket;

function initializePage(){
    $('#colScanner').hide();
    $('form#formStartScan').submit(formStartScan_submit);
    $('form#formDisconnect').submit(formDisconnect_submit);
    $('#formSaveSettings *').filter(':input').change(formSaveSettings_change);
    $('#inpFreqMax').keypress(inputKeyPress);
    $('#inpFreqMin').keypress(inputKeyPress);
    $('#inpDevIndex').keypress(inputKeyPress);
    $('#inpSampRate').keypress(inputKeyPress);
    $('#rngScanSensivity').attr('min', 1);
    $('#rngScanSensivity').attr('max', 10);
    $('#rngScanSensivity').val(5);
    $('#rngScanSensivity').on('input', rngScanSensivity_input);
}
function formStartScan_submit(event){
    if (graphActive){
        checkRange();
        stepSize = 2 * Math.pow(10, parseInt(Math.log10(maxFreq-minFreq)-1));
        maxRead = parseInt(maxFreq-minFreq)  / stepSize;
        currentRead = 0;
        currentFreq = parseInt($('#inpFreqMin').val());
        $('#divScanResults').text("");
        freqRes = [];
        dbRes = [];
        socket.emit('start_scan', currentFreq, parseInt($('#rngScanSensivity').val()));
    }else{
        currentFreq = maxFreq;
    }
    return false;
}
function formDisconnect_submit(event){
    socket.emit('disconnect_request');
    appendLog("Disconnecting...")
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
        'freq': parseInt($('#inpFreqMin').val()),
        'n': numRead,
        'i': interval
    };
    if(checkArgs(args))
        socket.emit('update_settings', args);
    else
        socket.emit('send_cli_args');
}
function rngScanSensivity_input(){
    $('#spnSensivity').text("Sensivity (" + $('#rngScanSensivity').val() + ")");
}
function inputKeyPress(evt){
    var charCode = (evt.which) ? evt.which : event.keyCode
    if (charCode > 31 && (charCode < 48 || charCode > 57))
        return false;
    return true;
}
function checkRange(){
    minFreq = parseInt($('#inpFreqMin').val());
    maxFreq = parseInt($('#inpFreqMax').val());
    if(maxFreq > minFreq)
        return true;
    return false;
}
function setRange(freq){
    $('#inpFreqMin').val(parseInt(+freq - (freq/5)));
    $('#inpFreqMax').val(parseInt(+freq + (freq/5)));
}
function checkArgs(args){
    if (args['dev'] < 0 || args['dev'] > 20 || args['samprate'] < 0 || 
    args['gain'] < 0  || args['i'] < 0 || !checkRange()){
        appendLog("Invalid settings detected.");
        $('#spnSettingsLog').text('Invalid settings detected.');
        setTimeout(function() {
            $('#spnSettingsLog').text('');
        }, 1000);
        $('#btnStartScan').prop("disabled", true);
        return false;
    }
    $('#btnStartScan').prop("disabled", false);
    return true;
}
function appendLog(msg){
    var currentTime = new Date().toLocaleTimeString().split(' ')[0];
    $('#divLog').append("<b>[" + currentTime + "]</b> " + msg + "<br>");
    $('#divLog').scrollTop($('#divLog').height());
}
function processRange(freqs, dbs){
    for (var i = 0; i < freqs.length; i++){
        var freq = freqs[i].toFixed(1);
        var db = dbs[i].toFixed(2);
        if(freqRes.indexOf(freq) == -1){
            freqRes.push(freq);
            dbRes.push(db);
            $('#divScanResults').append(freq + "<br>");
        }
    }
}
function updateProgress(){
    if(currentRead < maxRead){
        var percentage = parseInt((currentRead * 100) / maxRead);
        currentRead++;
        $('#lgScanResults').text('Scan Results [%' + percentage + ']');
    }else{
        $('#lgScanResults').text('Scan Results [%100]');
    }
}
function documentReady(){
    initializePage();
    socket = io.connect(location.protocol + '//' + document.domain + 
                 ':' + location.port + scanNamespace);

    socket.on('connect', function() {
        socket.emit('send_cli_args');
    });

    socket.on('log_message', function(log) {
        appendLog(log.msg);   
    });

    socket.on('dev_status', function(status) {
        if(parseInt(status) == 0){
            $('#formSaveSettings :input').prop('disabled', false);
            $('#formDisconnect :input').prop('disabled', false);
            graphActive = true;
            $('#btnStartScan').val("Start Scan");
            $('#lgScanResults').text("Scan Results");        
        }else if(parseInt(status) == 1) {
            $('#formSaveSettings :input').prop('disabled', true);
            $('#formDisconnect :input').prop('disabled', true);
            graphActive = false;
            $('#btnStartScan').val("Stop Scan");
            $('#spnFreqRange').text(minFreq + "-" + maxFreq);
        }
    });

    socket.on('graph_data', function(data) {
        $('#imgFreqScan').attr("src", "data:image/png;base64," + data.fft);
        processRange(data.freqs, data.dbs);
        updateProgress();
        if(!$('#colScanner').is(':visible'))
            $('#colScanner').show();
        currentFreq += stepSize;
        if(currentFreq<maxFreq){
            socket.emit('restart_sdr', currentFreq);
        }else{
            socket.emit('stop_sdr');
        }
    });

    socket.on('new_freq_set', function(status) {
        socket.emit('start_sdr', -1);
    });

    socket.on('cli_args', function(cliArgs) {
        var args = cliArgs.args;
        for (var i in args){
            if (i != 'freq')
                args[i] = args[i] || 0;
        }
        $('#inpDevIndex').val(args.dev);
        $('#inpSampRate').val(args.samprate);
        $('#inpDevGain').val(args.gain);
        interval = args.i;
        centerFreq = args.freq;
        numRead = args.n;
        if (cliArgs.status == 1){
            $('#spnSettingsLog').text('Settings saved.');
            setTimeout(function() {
                $('#spnSettingsLog').text('');
            }, 1000);
        }else{
            if(centerFreq > 0)
                setRange(centerFreq);
        }
        checkArgs(args);
    });

    socket.on('server_pong', function() {
        var latency = (new Date).getTime() - startTime;
        pingPongTimes.push(latency);
        pingPongTimes = pingPongTimes.slice(-30);11
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