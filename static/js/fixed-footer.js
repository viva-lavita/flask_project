$(document).ready(function() {
  $(window).on("load", function() {
    if ($(document).height() <= $(window).height()) {
      $(".page-footer").addClass("fixed-bottom");
      $(".featurette-divider").addClass("fix-bot");
    }
  });
});