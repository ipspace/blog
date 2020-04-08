$(function() {
  var server = 'https://my.ipspace.net/';
  if (location.host.indexOf('localhost') >= 0) {
    server = 'http://my.local:8080/'
  }
  $(".post__comment-add").click(function () {
    $("#post__comment-form").load(server+"bin/comment/get");
  });

  var comments = $("#comments");
  if (comments.length) {
    var recent = $("<div id='recent_comments' style='clear: both;'></div>");
    recent.appendTo($("#comments"));
    recent.load(server+"bin/comment/list");
  }
});
