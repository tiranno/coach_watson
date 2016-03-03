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

  $('#page-mask').on('tapone', drawerClose);
  $('#page-mask').on('click', drawerClose);

  $('#input-menu').on('tapone', drawerExpand);
  $('#input-menu').on('click', drawerExpand);
});
