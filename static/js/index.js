$(function () {
    var ws = new WebSocket('ws://' + window.location.host + '/ws');
    ws.onopen = function() {
    };
    ws.onmessage = function(evt) {
        $('#answer-text').text(evt.data);
    }

    $('#ask-button').click(function() {
        ws.send($('#ask-text').val());
        $('#ask-text').val('');
    });
});
