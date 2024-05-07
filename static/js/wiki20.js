// var debug = 1;

function tryLog(t) { try { if (debug) console.log(t); } catch(e) {} }

function h2ToTabs() {
  if ($(".no-tabs").length) { tryLog("No tabs"); return; }
  if ($("#tabs").length) { tryLog("Already have tabs"); return; }
    
  var divCnt;
  var tabDiv = $("<div id='tabs' class='no-tabs'></div>");
  
  var ul = $("<ul></ul>");
  var tabopts = {};
  var hashTag = location.hash;
  var childCnt = -1;
  
  function clickTab(evt) {
    var target = $(this).attr("href");
    var tabcnt = 0;
    var tabs = $("#tabs");
    tabs.find("li a").each(function() {
      if ($(this).attr("href") == target) { 
        tabs.tabs("option","selected",tabcnt); 
        if (evt) evt.preventDefault;
      }
      tabcnt++;
    });
    return false;
  }

  $("#left-column").find('a[href^="#"]').click(clickTab);

  tabopts['active'] = 0;
  tryLog('hashtag='+hashTag);
  $("#left-column").children("h2").each(function() {
//    tryLog("Found child: "+$(this).html());
    var hdr = $(this); hdr.addClass('content-tab-header');
    var nxt = hdr.nextUntil("h2").not("a[name]:last");
    var anc = hdr.prev("a"); if (!anc.length) return;

    childCnt++;
    hdr.appendTo(tabDiv);
    var div = $("<div class='content-tab'></div>").appendTo(tabDiv);
    var id  = anc.attr('id');
    div.attr('id',id); anc.remove();
    nxt.appendTo(div);
    
    var hText = hdr.is(":has(span.mw-headline)") ? hdr.find("span.mw-headline").html() : hdr.html();
    ul.append("<li><a href='#"+id+"'>"+hText+"</a></li");
    if (hdr.is(".first") && !hashTag) { tabopts['active'] = childCnt; hashTag = true; }
    if (hText.match(/contents/i) && !hashTag) tabopts['active'] = childCnt;    
    if ('#'+id == hashTag) tabopts['active'] = childCnt;
    tryLog('id='+id);
  });
  
  $("#toc").hide();
  ul.prependTo(tabDiv);
  if (childCnt >= 0) tabDiv.appendTo("#left-column");
  $("#right-column h2:first").css("padding-top",0);
  $("#tabs").tabs(tabopts);
  ul.append("<li class='filler'></li>");
  $(document).scrollTop(0);
};

$(function() {
  var sndRight = $(".send-right"); 
  var leftCol  = $("#left-column");
  if (sndRight.length && !leftCol.length) {
    var pDiv = $("#content-wrapper .post");
    var cLink = pDiv.find("#catlinks:first").remove();
  
    pDiv.wrapInner("<div id='post-wrapper'><div id='left-column'></div></div>");
    $("#post-wrapper").append("<div id='right-column'></div><div class='visualClear'></div>");
    pDiv.find("h2.send-right,h3.send-right").nextUntil("h2,h3").andSelf().appendTo("#right-column");
    pDiv.append(cLink);
    $(".register-image").parentsUntil("div").parent().hide();
  }
  h2ToTabs();
});

$(function() {
  if ($(".make-tabs").length) { tryLog("makeTabs"); h2ToTabs(); }
});

$(function() {

  function wrapAnswers() {
    var answers = $('#answers');
    var h3,answer;

    answers.children('div[id]').addClass('answerBody');
    while (1) {
      h3 = answers.children('h3').first(); if (!h3.length) return;
      console.log('Found answer H3');
      var div = $("<div class='answerBody'></div>");
      div.insertBefore(h3);
      answer = h3.nextUntil("h3,div[id],h2");
      console.log('Answer: '+h3.html()+' length '+answer.length);
      answer.detach();
      div.append(h3);
      div.append(answer);
      div.append("<p class='clear'></p>");
    }
  }

  $(".moreDocsLink a").click(function() { $(this).parents("td:first").find("div").show(); return false; });
  $(".grades .stars").each (function() {
    var me = $(this);
    var val = parseFloat(me.html());
    if (val <= 5 && val >= 1) {
      var sLeft = 1 + (5 - Math.floor(val + 0.75))*13;
      var sDown = Math.abs(val - Math.floor(val) - 0.5) < 0.25 ? 20 : 0;
      me.css({display: 'inline-block', width: '65px', height: '13px', marginRight: '1em',
	      background: 'white url(/images/stars.png) top left no-repeat',
	      backgroundPosition: '-'+sLeft+'px -'+sDown+'px'});
      me.html("");
    }
  });
  $('#answers h3').append('<span class="top">[ <a href="#left-column">Top</a> ]</span>');
  wrapAnswers();
});

$(function() {

  function getParameterByName(name) {
    var match = RegExp('[?&]' + name + '=([^&]*)')
                    .exec(window.location.search);
    return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
  }

  var code = getParameterByName("code"); 
  if (code) $("input[name=buy_"+code+"]").attr("checked","yes");
});

$(function() {
  $("div[data-load]").each(function() {
    var d = $(this); d.load(d.attr("data-load"));
  });
});

// Custom page functions
$(function() {
  if (typeof customPageSetup == 'function') {
    customPageSetup();
  }
});
