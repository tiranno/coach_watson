$(function () {
  /* Side drawer functions*/
  var drawerExpand = function() {
    $('#panel-left').addClass('expanded');
    window.setTimeout(deB,100);
    return;
  };
  var deB = function() {
    $('#page-mask').addClass('visible');
  }
  var drawerClose = function() {
    $('#panel-left').removeClass('expanded');
    $('#page-mask').removeClass('visible');
    return;
  };
  var inputClear = function() {
    $('#query-bar').val('');
  }


  /* Event listeners */
  // Issues with sideway scrolling currently (get rid of sideways scroll)
  // $('#panel-center').on('swiperight', drawerExpand);
  // $('#panel-center').on('swipeleft', drawerClose);
  $('#page-mask').on('tap', drawerClose);
  $('#page-mask').on('click', drawerClose);
  $('#input-menu').on('tap', drawerExpand);
  $('#input-menu').on('click', drawerExpand);

  $('#input-clear').on('tap click', inputClear);


});
