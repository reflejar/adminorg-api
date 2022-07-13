(function ($) {

  'use strict';

  function initNavbar() {

      $('.navbar-toggle').on('click', function (event) {
          $(this).toggleClass('open');
          $('#navigation').slideToggle(400);
      });

      $('.navigation-menu>li').slice(-2).addClass('last-elements');

      $('.navigation-menu li.has-submenu a[href="#"]').on('click', function (e) {
          if ($(window).width() < 992) {
              e.preventDefault();
              $(this).parent('li').toggleClass('open').find('.submenu:first').toggleClass('open');
          }
      });
  }
  // === following js will activate the menu in left side bar based on url ====
  function initMenuItem() {
      $(".navigation-menu a").each(function () {
          if (this.href == window.location.href) {
              $(this).parent().addClass("active"); // add active to li of the current link
              $(this).parent().parent().parent().addClass("active"); // add active class to an anchor
              $(this).parent().parent().parent().parent().parent().addClass("active"); // add active class to an anchor
          }
      });
  }
  function init() {
      initNavbar();
      initMenuItem();
  }

  init();

})(jQuery);




  $(window).load(function() {
    $(".se-pre-con").fadeOut("slow");;
  });

  $(function(){
    $('form').submit(function (e) {
        if ($(this).valid()) {
          $(this).find("button:submit").prop("disabled", true).append(' <i class="fa fa-spin fa-spinner"></i>');
          return true;
        } else {
          e.preventDefault();
          return false;
        }
    });
  });
  $("form").attr('autocomplete', 'off');