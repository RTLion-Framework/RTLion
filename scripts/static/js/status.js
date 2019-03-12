$(document).ready(clientStatus);

var clientJS;
function clientStatus(){
    clientInfo = getClientInfo();
    $("#spnClientInfo").text(JSON.stringify(clientInfo, null, 2));
    $("#spnClientInfo").hide();
    //window.location.replace("/");
}
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
    return clientInfo;3
}
