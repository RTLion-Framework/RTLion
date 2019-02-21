$(document).ready(graphSocket);
function graphSocket() {
    $('#fft_graph_column').hide();
    graph_namespace = '/graph';
    create_graph = true;
    var socket = io.connect(location.protocol + '//' + document.domain + 
                 ':' + location.port + graph_namespace);

    socket.on('connect', function() {
        socket.emit('send_cli_args');
    });

    socket.on('client_message', function(msg) {
        $('#log').append(msg.data + '<br>');
        $('#log').scrollTop($('#log').height());
    });
    $('form#create_graph').submit(function(event) {
        if (create_graph){
            // Check arguments
            create_graph = false;
            $('#btn_graph').val("Stop");
            read_count = 0;
            socket.emit('create_fft_graph');
        }else{
            create_graph = true;
            $('#btn_graph').val("Create FFT graph");
            socket.emit('stop_sdr');
        }
        return false;
    });

    socket.on('fft_data', function(msg) {
        $('#fft_graph').attr("src", "data:image/png;base64," + msg.data);
        read_count++;
        if($('#n_read').val() == "-1"){
            $('#read_count').text('(' + read_count + '/∞)');
        }else{
            $('#read_count').text('('+ read_count+ '/' + $('#n_read').val() + ')');
        }
        if(!$('#fft_graph_column').is(':visible')){
            $('#fft_graph_column').show();
        }
    });

    socket.on('cli_args', function(cliargs) {
        args = cliargs.args;
        $("#dev_index").val(args.dev);
        $("#samp_rate").val(args.samprate);
        $("#dev_gain").val(args.gain);
        $("#center_freq").val(args.freq);
        $("#n_read").val(args.n)
        $("#interval").val(args.i);
        read_count = args.n;
        if (cliargs.status == 1){
            $('#settings_log').text('Settings saved.');
            setTimeout(function() {
                $('#settings_log').text('');
            }, 1000);
        }
    });
    $('#save_settings *').filter(':input').change(function() {
        // Check arguments here
        socket.emit('update_settings',
        {'dev': parseInt($('#dev_index').val()), 
        'samprate': parseInt($('#samp_rate').val()), 
        'gain': $('#dev_gain').val(), 
        'freq': parseInt($('#center_freq').val()),
        'n': parseInt($('#n_read').val()),
        'i': parseInt($('#interval').val())});
    });
    var ping_pong_times = [];
    var start_time;
    var read_count;
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
        $('#ping_pong').text(Math.round(10 * sum / ping_pong_times.length) / 10 + "ms");
    });

}