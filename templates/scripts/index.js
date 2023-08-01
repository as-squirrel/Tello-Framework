function loadPage(page) {
    $.ajax({
        url: page,
        dataType: 'html',
        success: function(data) {
            $('.content').html(data);
        }
    });
}
function sendCommand(command) {
    $.ajax({
        type: 'POST',
        url: '/',
        data: { 'command': command },
        success: function(data) {
            console.log('Command sent: ' + command);
        }
    });
}