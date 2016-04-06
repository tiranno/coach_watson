$(function () {
  /* Fucntions for updating the dialog stream */
    // Websocket with server to preprocess sumbissions before sending to Watson
    var ws = new WebSocket('wss://' + window.location.host + '/ws');
    ws.onopen = function() {
    };
    ws.onmessage = function(evt) {
      printAnswer( evt.data );
    }
    // Upon submission of a quesiton
    $('#query-group').submit(function(){
        var question_text = $('#query-bar').val();
        ws.send(question_text);
        $('#query-bar').val('');

        printQuestion( question_text );

        // Prevents page from reloading
        $('#cw-app-content').scrollTop(0);
        return false;
    });

  /* Question / Answer */
    var printQuestion = function ( question_text ) {
        var question = $('<div />', {
            'class': 'col-xs-12'
        });
        question.append($('<div />', {
            'class': 'md-card card-question bottom-16'
        }));
        question.children(0).append($('<div />', {
            'class': 'md-card-body',
            text: question_text
        }))
        var line_break = $('<hr/>')
        $('#center-dialog').prepend(line_break);
        $('#center-dialog').prepend(question);

        // Unhide the center-dialog and hide the placeholder
        if(!$('#center-dialog').hasClass('visible')) {
            $('#center-dialog').addClass('visible');
        }
        $('#no-content').addClass('invisible');
    }

    var printAnswer = function ( answer_text ) {
        var answer = $('<div />', {
            'class': 'col-xs-12'
        });
        answer.append($('<img />', {
            'src': '../static/res/watson_logo.png',
            'class': 'watson-pic'
        }));
        answer.append($('<div />', {
            'class': 'md-card card-answer bottom-16'
        }));

        if(answer_text[0] === '<') {
            answer.children(0).append($('<div class="md-card-heading default">I think this might work for you ...</div>'));
            answer.children(0).append($(answer_text));
        } else {
            answer.children(0).append($('<div />', {
                'class': 'md-card-body' ,
                text: answer_text
            }))
        }

        $('#center-dialog').prepend(answer);
    }

    var printQA = function ( qapair ) {
        printQuestion( qapair['question'] );
        printAnswer( qapair['answer'] );
    }

    var loadTenQA = function() {
        $.get( '/qahistory', function( data ) {
            if (!!data) {
                dataArr = JSON.parse( data );
                dataArr.reverse();
                for (var i = 0; i < dataArr.length; i++) {
                    printQA( dataArr[i] );
                }
            }
        });
    };

    // $('').on('scroll', function() {
    //     if($(this).scrollTop() + $(this).innerHeight() >= $(this)[0].scrollHeight) {
    //         loadTenQA()
    //     }
    // })
    loadTenQA();
});
