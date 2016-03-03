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

  $('#panel-center').on('swiperight', drawerExpand);
  $('#page-mask').on('tapone click', drawerClose);
  $('#drawer-exit').on('tapone click', drawerClose);
  $('#input-menu').on('tapone click', drawerExpand);
});
