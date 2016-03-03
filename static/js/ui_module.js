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
  $('#panel-center').on('swipeleft', drawerExpand);

  $('#page-mask').on('tap', drawerClose);
  $('#page-mask').on('click', drawerClose);

  $('#input-menu').on('tap', drawerExpand);
  $('#input-menu').on('click', drawerExpand);
});
