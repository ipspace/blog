var isMainPage = 0;
var hideCount = 0;
var postURL = '';

function dw(t) { document.write(t); }
function setMainPage() { isMainPage = 1; }

function startHide() {
  hideCount ++ ;
  if (!isMainPage) { dw('<div id="show_'+hideCount+'">') ; return; }
  dw ('<p class="hideMenu"><a href="' +
    (postURL ? postURL : ('javascript:showRest(this)')) + 
    '">More ...</a></p>');
  dw ('<div style="display: none;">');
}

function showRest(t) {
  $(t).parents('p:first').hide().siblings('div').show();
}

function endHide() { dw ('</div>') ; }

$(function() {
/** Share-it fixup **/
  $("a[data-tpt]").each(function() {
    this.href = this.getAttribute('data-tpt').replace('%u%',escape(location)).replace('%t%',escape(document.title));
  });

/** Image link fixup **/
  $(".post a:has(img)").css("border-bottom","none");

/** Preview fixup **/
  if ($("div.blogger-clickTrap").length) {
    $("a[name=more]").css({
      "display"    : "block",
      "width"      : "100%",
      "height"     : "2px",
      "background" : "#F00"});
  }
});

var maxNumberOfPostsPerLabel = 10;
var maxNumberOfLabels = 3;
var blogHomeURL;
var labelCount = 0;
var relatedCache = {};
var skipEntries = { workshop:1, gestaltit: 1 }

function listRelatedEntries(json) {
  var ul = $("<ul>");
  var maxPosts = Math.min(json.feed.entry.length,maxNumberOfPostsPerLabel);
  var postCount = 0;

  for (var i = 0; i < maxPosts; i++) {
    var entry = json.feed.entry[i];
    var alturl;

    for (var k = 0; k < entry.link.length; k++) {
      if (entry.link[k].rel == "alternate") {
        alturl = entry.link[k].href; break;
      }
    }
    if (alturl && alturl != location.href && !relatedCache[alturl]) {
      ul.append("<li><a href='"+alturl+"'>"+entry.title.$t+"</a></li>");
      postCount++;
      relatedCache[alturl] = 1;
    }
  }

  if (!postCount) return;
  for (var l = 0; l < json.feed.link.length; l++) {
    if (json.feed.link[l].rel == "alternate") {
      var raw = json.feed.link[l].href;
      var label = raw.replace(/^.*\//,''); /* .substr(blogHomeURL.length+13); */
      label = label.replace(/%20/g, " ");
      var relatedDiv = $("#related_posts");
      if (relatedDiv.length) {
        var txt = unescape(label.substr(0,1).toUpperCase()+label.substr(1));
        var h = $("<h4><a href='"+raw+"'>"+txt+"</a></h4>");
        if (labelCount ++) h.addClass('next');
        relatedDiv.append(h);
        relatedDiv.append(ul);
      }
      break;
    }
  }
}

function searchRelatedPosts(query, label) {
  $.getScript(query + "feeds/posts/default/-/" + label +
				"?alt=json-in-script&callback=listRelatedEntries");
}

var previousLabels = {};
var remainingLabels = maxNumberOfLabels;

function displayRelatedPosts(textLabel) {
  if (previousLabels[textLabel] || remainingLabels <= 0 || skipEntries[textLabel.toLowerCase()]) return;

  previousLabels[textLabel] = true;
  remainingLabels --;
  
  searchRelatedPosts(blogHomeURL,textLabel);
}

$(function() {
  if (typeof blogLabels != 'undefined' && blogLabels instanceof Array) {
    for (var i = 0; i < blogLabels.length; i++) {
      displayRelatedPosts(blogLabels[i]);
    }
  }
})

function moveInFront(content,position) {
  $("#"+position).before($("#"+content));
}

var EVBC = function() {

  function dbg(t) {
    try { console.log(t); } catch(e) {}
  }
  
  var oneDay = 24 * 3600 * 1000;
  var now = new Date();
  
  function getConvertZone(z) {
    return (z == 'GMT-0500' || z == 'GMT-0400') ? "US-NY" : 
           (z == 'GMT+0100' || z == 'GMT+0200') ? "DE" : "SI";
  }
  
  function getZoneHours(h,z) {
    return /GMT(\W*\d{2})/.test(z) ? h + parseInt(RegExp.$1) : h;
  }

  function otherZones(d,z) {
    return "http://www.worldtimeserver.com/convert_time_in_"+getConvertZone(z)+".aspx?"+
           "y="+d.getFullYear()+"&mo="+(d.getUTCMonth()+1)+"&d="+d.getUTCDate()+"&h="+getZoneHours(d.getUTCHours(),z)+"&mn="+d.getMinutes();
  }
  
  function displayZone(z) {
    if (z == 'GMT-0500') return " EST";
    if (z == 'GMT-0400') return " EDT";
    if (z == 'GMT+0100') return " CET";
    if (z == 'GMT+0200') return " CEDT";
    return "";
  }
  
/*  function getLocalTimeZone(d) {
    var timeString = d.toString();
    var TZ = timeString.indexOf('(') > -1 ? 
	timeString.match(/\([^\)]+\)/)[0].match(/[A-Z]/g).join('') :
	timeString.match(/[A-Z]{3,4}/)[0];
    if (TZ == "GMT" && /(GMT\W*\d{4})/.test(timeString)) TZ = RegExp.$1;  
    return TZ;
  } */

  function getLocaleTimeString(d,z) {
    if (/GMT(\W*\d{2})/.test(z)) {
      var tzOffset = -parseInt(RegExp.$1) * 60; if (tzOffset == d.getTimezoneOffset()) return "";
    }
    var t = d.toLocaleTimeString();
    if (/(\d+:\d+):\d+(.*)/.test(t)) t = RegExp.$1+RegExp.$2;
    if (/(.*)GMT(.*)/.test(t)) t = RegExp.$1;
    return "( "+t + " your local time" + " )<br />";
/*  return "( "+t + " " + getLocalTimeZone(d)+" )<br />"; */
  }

  function displayEventData(evt,d) {
    d.append("<div class='calshadow'></div>");
    var img = "";
    if (evt.free) {
      img = "<img style='float: right; padding-left: 4px' src='http://www.ipSpace.net/images/ipSpace-free.png'>";
    }
    d.append("<p class='ebeventname'>"+img+"<a href='"+evt.link+"'>"+evt.title+"</a></p>");
    d.append("<p class='ebeventdate'>"+evt.string_start_date.replace(/, \d+/,"")+displayZone(evt.timezone)+"<br />"+
             getLocaleTimeString(evt.start_date,evt.timezone)+
             "<a href='"+otherZones(evt.start_date,evt.timezone)+"' target='_blank'>Convert to another time zone</a></p>");
    d.append("<p class='registernowbutton'><a href='"+evt.link+"' title='Click to register'>Register Now!</a></p>");
  }
  
  function displayUpcomingEvent(evt) {
    var w = $(".upcomingEvents"); if (!w.length) return;
    var r = Math.floor((evt.start_date - now) / oneDay);
    var d = w.html("<div id='ebcountdown'></div>").find("div");
    if (r > 0) {
      d.append("<div id='countdown'><h1>"+r+"</h1><p>Days remaining until</p></div>");
    } else {
      d.append("<div id='countdown'><h1 class='last' style='font-size: 65px;'>LAST<br />CALL</h1></div>");
    }
    displayEventData(evt,d);
    w.parents("DIV.widget").slideDown("slow");
  }

  function displayMoreEvents(evt) {
    var w = $(".upcomingEvents"); if (!w.length) return;
    var h = w.attr("data-href");
    if (h) { w.find("div#ebcountdown")
              .append("<div class='calshadow'></div>")
              .append("<p class='registernowbutton'><a href='"+h+"'>More events</a></p>"); }
  }
     
  function equalDate(a,b) {
    return (a.getFullYear() == b.getFullYear()) && 
    	   (a.getMonth() == b.getMonth()) &&
    	   (a.getDate() == b.getDate())
  }

  function loadEvents(v) {
//    displayCalendar(v.organizer.events[0]); return;
    var fd,evm,evc;
    
    evm = 0; evc=0;
    for (var i = 0; i < v.organizer.events.length; i++) {
      var evt = v.organizer.events[i];
      if (typeof evt.start_date == 'string') evt.start_date = new Date(evt.start_date);
//      dbg('typeof='+typeof evt.start_date+' '+evt.start_date);
      if (evt.start_date - now >= 0) {
        evc++;
        if (fd && ! equalDate(fd,evt.start_date) && (evc > 3 || (evt.start_date - now) > (oneDay * 35))) { 
          evm++; break; 
        }
        if (fd) {     
          displayEventData(evt,$(".upcomingEvents div#ebcountdown")); continue;
        }
        displayUpcomingEvent(evt); 
        fd = evt.start_date;
      }
    }
    if (evm) { displayMoreEvents(evt); } 
  }

  function init() {
    var d = $(".upcomingEvents");
    d.parents("DIV.widget").hide();
    var s = d.attr("data-script");
    if (s) { $.getScript(s); }
  }
  
  $(init);
  return { load: loadEvents };
}();
