$(document).ready(appPageInit);

var app_namespace = '/app';
var socket;

function appPageInit(){
    socket = io.connect(location.protocol + '//' + document.domain + 
                 ':' + location.port + app_namespace);
    
    
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
