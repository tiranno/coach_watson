$(function () {
  /* Side drawer functions*/
  var drawerExpand = function() {
    $('#panel-left').addClass('expanded');
    $('#page-mask').addClass('visible');
    return;
  };
  var drawerClose = function() {
    $('#panel-left').removeClass('expanded');
    $('#page-mask').removeClass('visible');
    return;
  };

  $('#panel-center').on('swipeone', drawerExpand);
  $('#page-mask').on('tap click', drawerClose);
  $('#drawer-exit').bind('tap click', drawerClose);
  $('#input-menu').bind('tap click', drawerExpand);
});
