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

  jQuery('#panel-center').bind('swipeone', drawerExpand);
  jQuery('#page-mask').bind('tap click', drawerClose);
  jQuery('#drawer-exit').bind('tap click', drawerClose);
  jQuery('#input-menu').bind('tap click', drawerExpand);
});
