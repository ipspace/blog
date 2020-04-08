function remove_duplicate_comments() {
  var recent = $("#recent_comments");
  var static = $("#comments div.comments-content").first()

  recent.find("li.comment").each(function() {
    var me = $(this);
    var sme = static.find('li[id='+me.attr('id')+']');
    if (sme.length) {
      me.remove();
    }
  });
  if (recent.find("li.comment").length == 0) {
    recent.remove();
  }
}

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
    recent.load(server+"bin/comment/list",remove_duplicate_comments);
  }
});
