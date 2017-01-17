$(function(){
  $('#myCarousel').carousel();
});

$(function() {
$(window).scroll( function(){
$('.fadeInBlock').each( function(i){
    var bottom_of_object = $(this).position().top + $(this).outerHeight();
    var bottom_of_window = $(window).scrollTop() + $(window).height();
    /* Adjust the "200" to either have a delay or that the content starts fading a bit before you reach it  */
    bottom_of_window = bottom_of_window + 25;
    if( bottom_of_window > bottom_of_object ){
        $(this).animate({'opacity':'1'},500);
            }
        });
    });
});

gapi.load("auth2"; function() {
    gapi.auth2.init();
});

var auth = function() {
    var user = document.getElementById("")
    list[x].addEventListener("mouseover", changeHeading);
}