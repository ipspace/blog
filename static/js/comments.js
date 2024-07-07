function move_comment_to_parent(me,parent) {

  /* Simplest case - parent is already a reply. Add current comment after it and move on */
  wrapper = $("<div></div>");
  wrapper.append(me);

  if (parent.closest(".comment-replies").length) {
    parent.after(wrapper);
    return;
  }

  /* Parent is not a reply but has replies. Add current comemnt at the end of replies and move on */
  parent_reply = parent.find(".comment-replies ol");
  if (parent_reply.length) {
    parent_reply.append(wrapper);
    return;
  }

  /* Most complex case - parent does not have replies. Build the whole structure */
  parent.append(`
    <div class="comment-replies">
      <div class="comment-thread inline-thread">
        <ol />
      </div>
    </div>`);
  parent.find(".comment-replies ol").append(wrapper);
}

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
      return;
    }
    parent_id = me.attr('data-parent');
    if (parent_id) {
      var parent = $("#comments li[id="+parent_id+"]");
      if (parent.length) {
        move_comment_to_parent(me,parent);
      }
    }
  });
  if (recent.find("li.comment").length == 0) {
    recent.remove();
  }
}

function get_comment_server() {
  return location.host.indexOf('local') >= 0 ?
    'http://my.local:8080/' :
    'https://my.ipspace.net/';
}

function get_post_url() {
  url = location.pathname;
  if (url.indexOf('.html') >= 0) {
    return url;
  }
  url = url.replace(/\/$/, "");
  return url + '.html';
}

function add_comment_form(event) {
  var me = $(this)
  var comment_block = me.closest("li.comment")
  reply_url = ""

  if (comment_block.length) {
    reply_url = "&id="+comment_block.attr("id")
    /* comment_block.find(".post__reply-form") */
    comment_form = $("<div class='post__reply-form'></div>")
    me.replaceWith(comment_form);
    /* comment_block.append(comment_form) */
  } else {
    comment_form = $("#post__comment-form");
  }

  $.ajax({
      url: get_comment_server()+"bin/comment/get?url="+get_post_url()+reply_url,
      dataType: 'html',
      xhrFields: { withCredentials: true },
      success: function(data) { comment_form.html(data); },
      failure: function(xhr,err) { alert ('Cannot load the comments form: '+err); }
  });
}

function add_comment_reply_links() {
  $("div#comments li.comment .comment-content").after(
    '<a class="post__comment-link post__comment-reply">'+
    '<svg class="post__comments-icon"><use xlink:href="#icon-comments"></use></svg>'+
    'Reply'+
    '</a>')
  $(".post__comment-reply").click(add_comment_form);
}

function comment_postprocessing() {
  recent = $("#recent_comments");
  remove_duplicate_comments();
  if (recent.find("#_enable_reply").length) {
    console.log("Comment replies are enabled");
    add_comment_reply_links();
  }
}

$(function() {
  var server = get_comment_server()
  $(".post__comment-add").click(function () {
    $.ajax({
        url: server+"bin/comment/get?url="+get_post_url(),
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
    recent.load(server+"bin/comment/list?url="+get_post_url(),comment_postprocessing);
  }
});
