$(document).ready(appPageInit);

var app_namespace = '/app';
var socket;

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
        alert(args);
        /*$("#inpDevIndex").val(args.dev);
        $("#inpSampRate").val(args.samprate);
        $("#inpDevGain").val(args.gain);
        $("#inpCenterFreq").val(args.freq);
        $("#inpNumRead").val(args.n);
        $("#inpInterval").val(args.i);*/
    });
}

var clientJS;
function getClientInfo(){
    clientJS = new ClientJS();
    var clientInfo = { 
        "browserFingerprint"  :  clientJS.getFingerprint(),
        "browserInfo"         :  clientJS.getBrowser() + " (" + clientJS.getBrowserVersion() + ")",
        "osInfo"              :  clientJS.getOS() + " " + clientJS.getOSVersion() + " (" + clientJS.getCPU() + ")",
        "screenInfo"          :  clientJS.getScreenPrint(),
        "timeZoneInfo"        :  clientJS.getTimeZone(),
        "langInfo"            :  clientJS.getLanguage()
    }
    return JSON.stringify(clientInfo, null, 2);
}
