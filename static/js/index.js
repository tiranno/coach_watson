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
        if(evt.data[0] === '<') {
            answer.children(0).append($('<div class="panel-heading">I think this might work for you ...</div>'));
            answer.children(0).append($(evt.data));
        } else {
            answer.children(0).append($('<div />', {
                'class': 'panel-body' ,
                text: evt.data
            }))
        }
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
        var line_break = $('<div />', {
            'class': 'col-xs-12'
        })
        line_break.append('<hr>');
        $('#dialog-pane').prepend(line_break);
        $('#dialog-pane').prepend(question);
        // Prevents page from reloading
        return false;
    });

    $('#ask-button').click(function() {
        ws.send($('#mainquerybar').val());
        $('#mainquerybar').val('');
    });
});
