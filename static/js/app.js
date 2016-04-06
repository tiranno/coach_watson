$(function () {
  /* Fucntions for updating the dialog stream */
    // Websocket with server to preprocess sumbissions before sending to Watson
    var askWatsonBool = window.location.pathname;
    console.log(askWatsonBool);
    var ws = new WebSocket('ws://' + window.location.host + '/ws');
    ws.onopen = function() {
      // console.log(ws);
    };
    ws.onmessage = function(evt) {
      printAnswer( JSON.parse(evt.data) );
    }
    ws.onclose = function(evt) {
      ws = new WebSocket('ws://' + window.location.host + '/ws');
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
    var printQuestion = function ( question_text, pend ) {
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

        if( pend === 'append'){
            $('#center-dialog').append(question);
            $('#center-dialog').append(line_break);
        } else {
            $('#center-dialog').prepend(line_break);
            $('#center-dialog').prepend(question);
        }

        // Unhide the center-dialog and hide the placeholder
        if(!$('#center-dialog').hasClass('visible')) {
            $('#center-dialog').addClass('visible');
        }
        $('#no-content').addClass('invisible');
    }

    var printAnswer = function ( answer_text, pend ) {
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
        if( pend === 'append'){
            $('#center-dialog').append(answer);
        } else {
            $('#center-dialog').prepend(answer);
        }
    }

    var printQA = function ( qapair ) {
        printAnswer( qapair['answer'], 'append' );
        printQuestion( qapair['question'], 'append' );
    }

    var loadTenQA = function( id ) {
        $.get( '/qahistory', { fromid: id } )
        .done ( function( data ) {
            dataArr = JSON.parse( data );
            for (var i = 0; i < dataArr.length; i++) {
                printQA( dataArr[i] );
            }
        });
    };

    $('#cw-app-content').on('scroll', function() {
        if($(this).scrollTop() + $(this).innerHeight() >= $(this)[0].scrollHeight) {
            loadTenQA()
        }
    })
    loadTenQA();
});
