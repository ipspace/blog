$(function() {
  $(".post__comment-add").click(function () {
    $("#post__comment-form").load("https://my.ipspace.net/bin/comment/get");
  });

  var recent = $("<div id='recent_comments' style='clear: both;'></div>");
  recent.appendTo($("#comments"));
  recent.load("https://my.ipspace.net/bin/comment/list");
});
