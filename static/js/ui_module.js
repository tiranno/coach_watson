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

  $('#panel-center').bind('swiperight', drawerExpand);
  $('#page-mask').bind('tapone click', drawerClose);
  $('#drawer-exit').bind('tapone click', drawerClose);
  $('#input-menu').bind('tapone click', drawerExpand);
});
