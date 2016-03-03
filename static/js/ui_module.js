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
  $('#page-mask').on('tapone', drawerClose);
  $('#page-mask').on('click', drawerClose);
  $('#drawer-exit').on('tapone', drawerClose);
  $('#drawer-exit').on('click', drawerClose);
  $('#input-menu').on('tapone', drawerExpand);
  $('#input-menu').on('click', drawerExpand);
});
