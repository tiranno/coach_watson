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

  $('#panel-center').bind('swipeone', drawerExpand);
  $('#page-mask').bind('tap click', drawerClose);
  $('#drawer-exit').bind('tap click', drawerClose);
  $('#input-menu').bind('tap click', drawerExpand);
});
