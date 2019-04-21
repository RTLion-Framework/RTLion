$(document).ready(documentReady);

var appNamespace = '/app';
var args;
var clientJS;
var clientInfo;
var socket;

function documentReady(){
    socket = io.connect(location.protocol + '//' + document.domain + 
                 ':' + location.port + appNamespace);
    
    socket.on('connect', function() {
        socket.emit('send_app_args');
    });

    socket.on('cli_args', function(cliArgs) {
        args = cliArgs.args;
        for (var i in args){
            if (i != 'freq')
                args[i] = args[i] || 0;
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
    socket.emit('send_app_args');
    return JSON.stringify(args);
}
function checkArgs(args){
    if (args['dev'] < 0 || args['dev'] > 20 || args['samprate'] < 0 ||
     args['gain'] < 0 || args['i'] < 0 || args['n'] < -1){
        return false;
    }
    return true;
}
function setCliArgs(newArgs){
    try {
        newArgs = JSON.parse(newArgs);
        if(checkArgs(newArgs)){
            socket.emit('update_settings', newArgs);
            socket.emit('send_app_args');
        }    
    } catch (error){
        console.log(error);
    } 
}
function getGraph(){
    socket.emit('get_fft_graph');
}
function getScannedValues(sensivity){
    socket.emit('get_scanned_values', sensivity);
}