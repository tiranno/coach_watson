$(function () {
    var ws = new WebSocket('ws://' + window.location.host + '/ws');
    ws.onopen = function() {
    };
    ws.onmessage = function(evt) {
        var answer = $('<div />', {
            'class': 'col-xs-12'
        })
        answer.append($('<div />', {
            'class': 'panel panel-default panel-answer'
        }))
        answer.children(0).append($('<div />', {
            'class': 'panel-body',
            text: evt.data
        }))
        $('#dialog-pane').prepend(answer);
    }

    $('form').submit(function(){
        var question_text = $('#mainquerybar').val();
        ws.send(question_text);
        $('#mainquerybar').val('');
        var question = $('<div />', {
            'class': 'col-xs-12'
        })
        question.append($('<div />', {
            'class': 'panel panel-default panel-question'
        }))
        question.children(0).append($('<div />', {
            'class': 'panel-body',
            text: question_text
        }))
        $('#dialog-pane').prepend(question);
        // Prevents page from reloading
        return false;
    });

    $('#ask-button').click(function() {
        ws.send($('#mainquerybar').val());
        $('#mainquerybar').val('');
    });
});
