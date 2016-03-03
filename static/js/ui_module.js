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

  jQuery('#panel-center').bind('swiperight', drawerExpand);
  jQuery('#page-mask').bind('tapone click', drawerClose);
  jQuery('#drawer-exit').bind('tapone click', drawerClose);
  jQuery('#input-menu').bind('tapone click', drawerExpand);
});
