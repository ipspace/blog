function tryLog(t) {
  try {
    if (debug) console.log(t);
  } catch (e) {}
}

tryLog("main.js");

/** Fix login buttons **/
$(function() {
  var cookie = "; "+document.cookie;
  var isLoggedIn = cookie.indexOf("; usr=") >= 0;

  console.log(cookie);
  console.log(isLoggedIn);
  if (!isLoggedIn) { return; }
/* $(".hide-on-login").hide(); */

  var loginLink = $(".login-link");
  var headerCTA = $(".header-cta");

  headerCTA.html("my content").attr("href",loginLink.attr("href"));
  loginLink.html("logout").attr("href",loginLink.attr("href")+"/bin/profile/logout");

  $("a[data-login-url]").each(function() {
    var me = $(this);
    me.attr("href",me.attr("data-login-url"));
  })
});

$(function() {
  function sendToRight() {
    var sendRight = $(".send-right");
    var leftColumn = $("#left-column");

    if (sendRight.length && !leftColumn.length) {
      var post = $("#content-wrapper .post");
      var h1 = post.find(".firstHeading").remove();

      post.wrapInner("<div id='left-column'></div>");
      post.prepend(h1);
      post.append("<div id='right-column'></div>");
      post
        .find("h2.send-right,h3.send-right")
        .nextUntil("h2,h3")
        .addBack()
        .appendTo("#right-column");
      post.addClass("flex");
      return true;
    }
  }

  function clickTab(evt) {
    var target = $(this).attr("href");

    $("#tabs .ui-tabs-nav li a").each(function() {
      if ($(this).attr("href") == target) {
        $(this).click();
        if (evt) evt.preventDefault;
      }
    });
    return false;
  }

  function headersToTabs(force) {
    if ($(".no-tabs").length && !force) {
      tryLog("No tabs");
      return;
    }
    if ($("#tabs").length) {
      tryLog("Already have tabs");
      return;
    }

    if ($("#left-column > h2").length < 2) {
      tryLog("Not enough H2 headings for tabs");
      return;
    }

    var divCnt;

    var hashTag = location.hash;
    var childCnt = 0;
    var activeTab = 0;

    var tabDiv = $("<div id='tabs' class='ui-tabs no-tabs'></div>");

    var ul = $("<ul class='ui-tabs-nav'></ul>");

    tryLog("hashtag=" + hashTag);

    $("#left-column")
      .children("h2")
      .each(function() {
        //    tryLog("Found child: "+$(this).html());
        var hdr = $(this);
        hdr.addClass("content-tab-header");
        var nxt = hdr.nextUntil("h2").not("a[name]:last");
        var anc = hdr.prev("a");
        if (!anc.length) return;

        childCnt++;
        hdr.appendTo(tabDiv);
        var div = $("<div class='content-tab'></div>").appendTo(tabDiv);
        var id = anc.attr("id");
        div.attr("id", id);
        anc.remove();
        nxt.appendTo(div);

        var hText = hdr.is(":has(span.mw-headline)")
          ? hdr.find("span.mw-headline").html()
          : hdr.html();
        ul.append("<li><a href='#" + id + "'>" + hText + "</a></li");

        if (hashTag) {
          if ("#" + id == hashTag) activeTab = childCnt;
        } else {
          if (hText.match(/contents/i)) activeTab = childCnt;
        }
      });

    if (childCnt > 0) {
      /* Insert tabs into markup */
      $("#left-column")
        .find('a[href^="#"]')
        .click(clickTab);
      $("#toc").hide();
      ul.prependTo(tabDiv);
      ul.append("<li class='filler'></li>");
      tabDiv.appendTo("#left-column");
      return activeTab || 1;
    }
    /* $("#right-column h2:first").css("padding-top",0); */
    /* $("#tabs").tabs(tabopts); */
  }

  function doTabs() {
    var tabs = $("#tabs");

    if (tabs.length > 0) {
      var navItems = tabs.find(".ui-tabs-nav li"),
        contentTabs = tabs.find(".content-tab");

      tabs.addClass("js-tabs");

      navItems.each(function() {
        $(this)
          .find("a")
          .on("click", function(e) {
            e.preventDefault();

            // toggle activeness of the nav tabs
            $(this)
              .parent()
              .addClass("ui-state-active")
              .siblings()
              .removeClass("ui-state-active");

            // hide and show content tabs
            var target = $(this).attr("href");

            contentTabs.addClass("ui-tabs-hide");
            $(target).removeClass("ui-tabs-hide");
          });
      });
    }
  }

  function wrapAnswers() {
    var answers = $("#answers");
    var h3, answer;

    // console.log("wrapping answers: "+answers.length);
    answers.children("div[id]").addClass("content-box tiny-margin");
    while (1) {
      h3 = answers.children("h3").first();
      if (!h3.length) return;
      // console.log('Found answer H3');
      var div = $("<div class='content-box tiny-margin'></div>");
      div.insertBefore(h3);
      answer = h3.nextUntil("h3,div[id],h2");
      // console.log('Answer: '+h3.html()+' length '+answer.length);
      answer.detach();
      div.append(h3);
      div.append(answer);
      div.append("<span class='visualClear'></span>");
    }
  }

  var singleColumn = sendToRight();
  var activeTab = 0;
  var makeTabs = $(".make-tabs").length;

  if (singleColumn || makeTabs) {
    activeTab = headersToTabs(makeTabs);
  }
  doTabs();
  if (activeTab) {
    var tabToGo = $("#tabs .ui-tabs-nav li:nth-child(" + activeTab + ") a");
    tabToGo.click();
    if (location.hash) {
      $(document).scrollTop(tabToGo.offset().top);
    } else {
      $(document).scrollTop(0);
    }
  } /* click on desired tab to make it active */

  $(".planCompare").wrap('<div class="planCompare__wrap"></div>');
  wrapAnswers();

  var rightColumn = $("#right-column");
  if (rightColumn.length) {
    $(".post").prepend("<a href='#' class='open-sidebar'>Sidebar</a>");
    rightColumn.prepend(
      "<div class='sidebar__mobile-nav'>" +
        "<a href='#' class='close-sidebar'><svg class='close-icon'><use xlink:href='#icon-close'/></svg></a>" +
        "</div>"
    );
  }

  $("#open-editing-sidebar").click(function(e) {
    e.preventDefault();
    $("#mw_portlets").toggle();
    $(this).blur();
  });

  var userIncrementers = $(".userIncrementer");

  userIncrementers.each(function() {
    var userCountEl = $(this).find(".usersInPlan__count"),
      userCount = parseInt(userCountEl.text());

    $(this)
      .find(".btnPlus")
      .on("click", function(e) {
        e.preventDefault();
        userCount++;
        userCountEl.text(userCount);
      });

    $(this)
      .find(".btnMinus")
      .on("click", function(e) {
        e.preventDefault();
        if (userCount > 1) userCount--;
        userCountEl.text(userCount);
      });
  });

  $(".btnPlus").on("click", function(e) {
    e.preventDefault();
    var users = $();
  });
});
