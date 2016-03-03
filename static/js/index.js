$(function () {
  /* Fucntions for updating the dialog stream */
    // Websocket with server to preprocess sumbissions before sending to Watson
    var ws = new WebSocket('wss://' + window.location.host + '/ws');
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
        $('#center-dialog').prepend(answer);
    }
    // Upon submission of a quesiton
    $('form').submit(function(){
        var question_text = $('#query-bar').val();
        ws.send(question_text);
        $('#query-bar').val('');
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
        $('#center-dialog').prepend(line_break);
        $('#center-dialog').prepend(question);
        // Unhide the center-dialog and hide the placeholder
        if(!$('#center-dialog').hasClass('visible')) {
            $('#center-dialog').addClass('visible');
        }
        $('#no-content').addClass('invisible');
        // Prevents page from reloading
        return false;
    });
});
