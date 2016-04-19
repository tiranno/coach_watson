$(function () {
    // functions
    var addExercise = function( data ) {

      // normal
        var subrow0 = $('<div />', {'class': 'col-xs-4'});
        subrow0.append( data['name'] );
        var subrow1 = $('<div />', {'class': 'col-xs-5'});
        subrow1.append( data['amount'] );
        var subrow2 = $('<div />', {'class': 'col-xs-3'});
        subrow2.append( $('<button />', {
            'id': 'add-workout',
            'class': 'md-button flat',
            'style': 'float: right;'
        }) );
        subrow2.children(0).append( $('<i />', {
            'class': 'material-icons',
            text: 'mode_end'
        }) );
        var normal = $('<li />', {'id': '?', 'class': 'invisible'}).append(subrow0, subrow1, subrow2);

      // edit
        var subrow0 = $('<div />', {'class': 'col-xs-4'});
        subrow0.append( $('<input />', {
            'name': 'exer-name',
            'placeholder': 'Name',
            'type': 'text'
        }) );
        var subrow1 = $('<div />', {'class': 'col-xs-5'});
        subrow1.append( $('<input />', {
            'name': 'exer-amnt',
            'placeholder': 'Amount',
            'type': 'text'
        }) );
        var subrow2 = $('<div />', {'class': 'col-xs-3'});
        subrow2.append( $('<button />', {
            'id': 'cancel-workout',
            'class': 'md-button flat',
            'style': 'float: right;',
            'html': '<i class="material-icons">cancel</i>'
        }) );
        subrow2.append( $('<button />', {
            'id': 'confirm-workout',
            'class': 'md-button flat',
            'style': 'float: right;',
            'html': '<i class="material-icons">check</i>'
        }) );
        var editing = $('<li />', {'id': '?', 'class': 'visible'}).append(subrow0, subrow1, subrow2);

        $('#workouts-list > ul').append(editing);
    }
    var editExercise = function() {
        id = this.id;
    }

    var getExercise = function() {
        $.ajax({
          url: '/workout/exercise',
          type: 'GET',
          success: function( data ) {
            // remove from list
          }
        });
    }
    var saveExercise = function() {
        $.ajax({
          url: '/workout/exercise',
          type: 'POST',
          data: {}, //{ 'dayid': this.id, 'name': , 'amount': }
          success: function( data ) {
            // remove from list
          }
        });
    }
    var delExercise = function() {
        $.ajax({
          url: '/workout/exercise',
          type: 'DELETE',
          success: function( data ) {
            // remove from list
          }
        });
    }

    // event listeners
    $('#add-workout').on('tap click', addExercise);
    // $('#del-exercise').on('tap click', delExercise);
    // $('#edit-exercise').on('tap click', editExercise);



    // functions
    var loadDay = function() {
        $.ajax({
            url: '/workout/day',
            type: 'GET',
            data: { 'dayid': this.id }
        }).done(function( exerArr ) {
            console.log(exerArr);
            // clearBody();
            // for (var i = 0; i < exerArr.length; i++) {
            //     addExercise( exerArr[i] );
            // }
        });
    }
    var clearBody = function() {
        $('#workouts-list').empty();
    }
    var loadExercises = function() {

    }

    // event listeners
    $('#0, #1, #2, #3, #4, #5, #6').on('tap click', loadDay);

});
