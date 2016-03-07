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

  // Issues with sideway scrolling currently (get rid of sideways scroll)
  // $('#panel-center').on('swiperight', drawerExpand);
  // $('#panel-center').on('swipeleft', drawerClose);

  $('#page-mask').on('tap', drawerClose);
  $('#page-mask').on('click', drawerClose);

  $('#input-menu').on('tap', drawerExpand);
  $('#input-menu').on('click', drawerExpand);
});
