var toggleRecordingGlobal = null;   // Uglyish workaround
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
      ws = new WebSocket('wss://' + window.location.host + '/ws');
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
            'html': question_text
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

        var script = answer_text;
        if(answer_text[0] === '<') {
            answer.children(0).append($('<div class="md-card-heading default">I think this might work for you ...</div>'));
            answer.children(0).append($(answer_text));
            script = 'I think this might work for you...'
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

        answer.click( function() {
          if( responsiveVoice.isPlaying() ) {
              responsiveVoice.cancel();
          } else {
              responsiveVoice.speak(script);
          }
        });
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




   ////////////////////////////////////////////
  //                                        //
 //                 S2T                    //
//                                        //
///////////////////////////////////////////

    /* Copyright 2013 Chris Wilson

       Licensed under the Apache License, Version 2.0 (the "License");
       you may not use this file except in compliance with the License.
       You may obtain a copy of the License at

           http://www.apache.org/licenses/LICENSE-2.0

       Unless required by applicable law or agreed to in writing, software
       distributed under the License is distributed on an "AS IS" BASIS,
       WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
       See the License for the specific language governing permissions and
       limitations under the License.
    */

    window.AudioContext = window.AudioContext || window.webkitAudioContext;

    var audioContext = new AudioContext();
    var audioInput = null,
        realAudioInput = null,
        inputPoint = null,
        audioRecorder = null;
    var rafID = null;
    var analyserContext = null;
    var canvasWidth, canvasHeight;
    var recIndex = 0;

    function saveAudio() {
        audioRecorder.exportWAV( doneEncoding );
        // could get mono instead by saying
        // audioRecorder.exportMonoWAV( doneEncoding );
    }

    function gotBuffers( buffers ) {
        var canvas = document.getElementById( "wavedisplay" + recIndex);

        drawBuffer( canvas.width, canvas.height, canvas.getContext('2d'), buffers[0] );

        // the ONLY time gotBuffers is called is right after a new recording is completed -
        // so here's where we should set up the download.
        audioRecorder.exportWAV( doneEncoding );
    }

    function doneEncoding( blob ) {
        console.log(blob);
        S2Tws.send(blob);
        S2Tws.send('{"action": "stop"}');
        // Recorder.setupDownload( blob, "myRecording" + ((recIndex<10)?"0":"") + recIndex + ".wav" );
        recIndex++;
    }

    function toggleRecording(e) {
        if (e.classList.contains("recording")) {
            // stop recording
            audioRecorder.stop();
            e.classList.remove("recording");
            printQuestion('<canvas id="wavedisplay' + recIndex + '" width="200" height="65" style="margin-top:-12px; margin-bottom:-12px;"></canvas');
            audioRecorder.getBuffers( gotBuffers );
        } else {
            // start recording
            if (!audioRecorder)
                return;
            e.classList.add("recording");
            audioRecorder.clear();
            audioRecorder.record();
        }
    }

    function convertToMono( input ) {
        var splitter = audioContext.createChannelSplitter(2);
        var merger = audioContext.createChannelMerger(2);

        input.connect( splitter );
        splitter.connect( merger, 0, 0 );
        splitter.connect( merger, 0, 1 );
        return merger;
    }

    function cancelAnalyserUpdates() {
        window.cancelAnimationFrame( rafID );
        rafID = null;
    }

    function updateAnalysers(time) {
        if (!analyserContext) {
            var canvas = document.getElementById("analyser");
            canvasWidth = canvas.width;
            canvasHeight = canvas.height;
            analyserContext = canvas.getContext('2d');
        }

        // analyzer draw code here
        {
            var SPACING = 2;
            var BAR_WIDTH = 1;
            var numBars = Math.round(canvasWidth / SPACING);
            var freqByteData = new Uint8Array(analyserNode.frequencyBinCount);

            analyserNode.getByteFrequencyData(freqByteData);

            analyserContext.clearRect(0, 0, canvasWidth, canvasHeight);
            analyserContext.fillStyle = '#F6D565';
            analyserContext.lineCap = 'round';
            var multiplier = analyserNode.frequencyBinCount / numBars;

            // Draw rectangle for each frequency bin.
            for (var i = 0; i < numBars; ++i) {
                var magnitude = 0;
                var offset = Math.floor( i * multiplier );
                // gotta sum/average the block, or we miss narrow-bandwidth spikes
                for (var j = 0; j< multiplier; j++)
                    magnitude += freqByteData[offset + j];
                magnitude = magnitude / multiplier;
                var magnitude2 = freqByteData[i * multiplier];
                //analyserContext.fillStyle = "hsl( " + Math.round((i*360)/numBars) + ", 100%, 50%)";
                analyserContext.fillStyle = "silver";
                analyserContext.fillRect(i * SPACING, canvasHeight, BAR_WIDTH, -magnitude);
            }
        }

        rafID = window.requestAnimationFrame( updateAnalysers );
    }

    function toggleMono() {
        if (audioInput != realAudioInput) {
            audioInput.disconnect();
            realAudioInput.disconnect();
            audioInput = realAudioInput;
        } else {
            realAudioInput.disconnect();
            audioInput = convertToMono( realAudioInput );
        }

        audioInput.connect(inputPoint);
    }

    function gotStream(stream) {
        inputPoint = audioContext.createGain();

        // Create an AudioNode from the stream.
        realAudioInput = audioContext.createMediaStreamSource(stream);
        audioInput = realAudioInput;
        audioInput.connect(inputPoint);

    //    audioInput = convertToMono( input );

        analyserNode = audioContext.createAnalyser();
        analyserNode.fftSize = 2048;
        inputPoint.connect( analyserNode );

        audioRecorder = new Recorder( inputPoint );

        zeroGain = audioContext.createGain();
        zeroGain.gain.value = 0.0;
        inputPoint.connect( zeroGain );
        zeroGain.connect( audioContext.destination );
        updateAnalysers();
    }

    function initAudio() {
            if (!navigator.getUserMedia)
                navigator.getUserMedia = navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
            if (!navigator.cancelAnimationFrame)
                navigator.cancelAnimationFrame = navigator.webkitCancelAnimationFrame || navigator.mozCancelAnimationFrame;
            if (!navigator.requestAnimationFrame)
                navigator.requestAnimationFrame = navigator.webkitRequestAnimationFrame || navigator.mozRequestAnimationFrame;

        navigator.getUserMedia(
            {
                "audio": {
                    "mandatory": {
                        "googEchoCancellation": "false",
                        "googAutoGainControl": "false",
                        "googNoiseSuppression": "false",
                        "googHighpassFilter": "false"
                    },
                    "optional": []
                },
            }, gotStream, function(e) {
                alert('Error getting audio');
                console.log(e);
            });
    }

    function drawBuffer( width, height, context, data ) {
        var step = Math.ceil( data.length / width );
        var amp = height / 2;
        context.fillStyle = "#98C0C5";
        context.clearRect(0,0,width,height);
        for(var i=0; i < width; i++){
            var min = 1.0;
            var max = -1.0;
            for (j=0; j<step; j++) {
                var datum = data[(i*step)+j];
                if (datum < min)
                    min = datum;
                if (datum > max)
                    max = datum;
            }
            context.fillRect(i,(1+min)*amp,1,Math.max(1,(max-min)*amp));
        }
    }

    function get_watson_S2T_token() {
        var token = '';
        $.ajax({
            url: '/speech_to_text',
            async: false,
            success: function(data){
                token = data;
            }
        });
        return token;
    }

    window.addEventListener('load', initAudio );

    var token = get_watson_S2T_token();
    var S2Tws = new WebSocket("wss://stream.watsonplatform.net/speech-to-text/api/v1/recognize?watson-token=" + token + "&model=en-US_BroadbandModel");
    S2Tws.onopen = function() {
        var start_message = '{"action": "start", "content-type": "audio/wav", "continuous":true}';
        S2Tws.send(start_message);
    };
    S2Tws.onmessage = function(evt) {
      console.log( evt.data );
      var res = JSON.parse(evt.data);
      if ('results' in res) {
          console.log(res['results']);
          if ('alternatives' in res['results'][0]) {
              var alt = res['results'][0]['alternatives'][0];
              console.log(alt);
              if ('transcript' in alt) {
                  var trans = alt['transcript'];
                  console.log(trans);
                  ws.send(trans);
              }
          }
      }
    }
    S2Tws.onclose = function(evt) {
      console.log('S2T WebSocket closed.');
    }
    S2Tws.onerror = function(evt) {
      console.log( evt.data );
    }
    // Keep S2Tws alive
    setInterval(function() { S2Tws.send('{"action": "no-op"}'); }, 25000);
    toggleRecordingGlobal = toggleRecording;

});
