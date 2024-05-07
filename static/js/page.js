console.log("ipSpace.js");
// Open mobile menu
$("#open-menu").on("click", function() {
  $("#mobile-menu").addClass("open");
  $("body").addClass("mobile-menu-active");
});

// Close mobile menu

$("#close-menu").on("click", function() {
  $("#mobile-menu").removeClass("open");
  $("body").removeClass("mobile-menu-active");
});

$(function (){
  $(".open-sidebar").on("click", function(e) {
    e.preventDefault();
    $("body").addClass("sidebar-active");
  });

  $(".close-sidebar").on("click", function(e) {
    e.preventDefault();
    $("body").removeClass("sidebar-active");
  });
});

//See more list items on sidebar
$(".sidebar__btn").on("click", function(e) {
  var additional_list = $(this).siblings(".additional-list");
  additional_list.toggleClass("open");
  if (additional_list.hasClass("open")) {
    $(this).text("see less");
  } else {
    $(this).text("see more");
  }
});

$(".open-dropdown").on("click", function(e) {
  var sib = $(this).siblings(".dropdown");
  $(this).toggleClass("open");
  sib.toggleClass("open");
  if (sib.length) {
    e.preventDefault();
    e.stopPropagation();
    return false;
  }
});

// Toggle searchBox for tablet viewports
var searchBtn = $("#search-btn"),
    searchInput = $("#search-input"),
    searchForm  = $(".search-form");

searchBtn.on("click", function(e) {
  if (searchInput.val() == "") {
    e.preventDefault();
    searchInput.toggleClass("active");
  }
});

//
// $(function() {
//   var openDropList = $("#ArchiveList .dropdown")
//     .has(".archive_posts")
//     .add(".archive_posts");
//   console.log(openDropList);
//   openDropList.addClass("open");
//   openDropList.siblings(".open-dropdown").addClass("open");
// });
