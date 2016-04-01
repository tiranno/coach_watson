$(function () {
  /* Top bar functions*/
    var drawerExpand = function() {
        $('#panel-left').addClass('expanded');
        window.setTimeout(deB,100);
        return;
    };
    var deB = function() {
        $('#page-mask').addClass('visible');
    };
    var drawerClose = function() {
        $('#panel-left').removeClass('expanded');
        $('#page-mask').removeClass('visible');
        return;
    };
    var inputClear = function() {
        $('#query-bar').val('');
    };

    /* Event listeners */
    $('#page-mask').on('tap click', drawerClose);
    $('#input-menu').on('tap click', drawerExpand);
    $('#input-clear').on('tap click', inputClear);
    // Issues with sideway scrolling currently (get rid of sideways scroll)
    // $('#panel-center').on('swiperight', drawerExpand);
    // $('#panel-center').on('swipeleft', drawerClose);



  /* Feedback dialog functions */
    var showFeedbackDialog = function() {
        $('#feedback-dialog').addClass('visible');
    };
    var hideFeedbackDialog = function() {
        $('#feedback-dialog').removeClass('visible');
        $('#feedback-text').empty();
        $('#fb-text').empty();
    };
    $('#feedback').on('tap click', showFeedbackDialog);
    $('#fb-clear').on('tap click', hideFeedbackDialog);
    $('#feedback-form').submit(function(event) {
        input = $("#fb-text").html();
        if(input == null || input == ""){
          return false;
        }
        $('#feedback-text').val($("#fb-text").html());

        $.ajax({
          url:'/form/feedback',
          type:'post',
          data:$('#feedback-form').serialize(),
          success:function(){
              hideFeedbackDialog();
          }
        });
        return false;
    });
    // $('#.fb-text').change(function(){
    //   ('#feedback-text').val(("#fb-text").html());
    // });


});
