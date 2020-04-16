function remove_duplicate_comments() {
  var recent = $("#recent_comments");
  var static = $("#comments div.comments-content");

  /* If there's a single comment-contents DIV then we can't compare old to recent */
  if (static.length <= 1) { return; }
  static = static.first()

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
    /*
    $("#post__comment-form").load(server+"bin/comment/get"); */
    $.ajax({
        url: server+"bin/comment/get",
        dataType: 'html',
        xhrFields: { withCredentials: true },
        success: function(data) { $("#post__comment-form").html(data); },
        failure: function(xhr,err) { alert ('Cannot load the comments form: '+err); }
    });
  });

  var comments = $("#comments");
  if (comments.length) {
    var recent = $("<div id='recent_comments' style='clear: both;'></div>");
    var cmtlist = $("#comments");
    recent.appendTo(cmtlist);
    recent.load(server+"bin/comment/list?url="+location.pathname,remove_duplicate_comments);
  }
});
