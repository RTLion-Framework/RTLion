$(document).ready(appPageInit);

var app_namespace = '/app';
var socket;
var rtlArgs;
var clientJS;
var clientInfo;

function appPageInit(){
    socket = io.connect(location.protocol + '//' + document.domain + 
                 ':' + location.port + app_namespace);
    
    socket.on('connect', function() {
        socket.emit('send_cli_args');
    });

    socket.on('cli_args', function(cliargs) {
        args = cliargs.args;
        for (var i in args){
            if (i != 'freq')
                args[i] = args[i] || 0;
        }
        rtlArgs = {
            "devIndex"      :  args.dev,
            "sampleRate"    :  args.samprate,
            "devGain"       :  args.gain,
            "centerFreq"    :  args.freq,
            "numRead"       :  args.n,
            "readInterval"  :  args.i
        }
    });
}

function getClientInfo(){
    clientJS = new ClientJS();
    clientInfo = { 
        "browserFingerprint"  :  clientJS.getFingerprint(),
        "browserInfo"         :  clientJS.getBrowser() + " (" + clientJS.getBrowserVersion() + ")",
        "osInfo"              :  clientJS.getOS() + " " + clientJS.getOSVersion() + " (" + clientJS.getCPU() + ")",
        "screenInfo"          :  clientJS.getScreenPrint(),
        "timeZoneInfo"        :  clientJS.getTimeZone(),
        "langInfo"            :  clientJS.getLanguage()
    }
    return JSON.stringify(clientInfo, null, 2);
}

function getCliArgs(){
    socket.emit('send_cli_args');
    return JSON.stringify(rtlArgs, null, 2);
}
function checkArgs(args){
    if (args['dev'] < 0 || args['dev'] > 20 || args['samprate'] < 0 ||
     args['gain'] < 0 || args['freq'] <= 0 || args['freq'] == "" || 
     isNaN(args['freq']) || args['freq'] == null || args['i'] < 0 || args['n'] < -1){
        return false;
    }
    return true;
}
function setCliArgs(newArgs){
    try {
        args = JSON.parse(newArgs);
        if(checkArgs(args)){
            socket.emit('update_settings', args);
            socket.emit('send_cli_args');
        }
        return JSON.stringify(rtlArgs, null, 2);
    } catch (err) {
        return err.message;
    }
}