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