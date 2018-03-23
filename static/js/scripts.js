// Logic for Preloader
$('nav').hide();
$('section').hide();
$('.preloader').show();
$('footer').hide();

$(window).on("scroll", function(){
	w = window.innerWidth;
	if (w > 700){
		if($(window).scrollTop() > 100){
			$('nav').show();
			$('nav').removeClass('slideOutUp');
			$('nav').addClass('slideInDown');
		}
		else{
			$('nav').removeClass('slideInDown');
			$('nav').addClass('slideOutUp');
		}
	}
})

$(window).on('load', function(){
	$('section').show();
	$('.preloader').addClass('animated slideOutUp');
	setTimeout(function(){
		$('.preloader').remove();
		$('footer').show();
		w = window.innerWidth;
		if (w < 700){
			$('nav').show();
		}
	},1000);
});


// Inview Loading for Parallax Images in Mobile View

if(window.innerWidth < 700){
	$("[class^=pw]").css('visibility','hidden');
	$("[class^=pw]").on('inview', function(event, isInView) {
	  if (isInView) {
	    $(this).css('visibility','visible');
	    $(this).addClass('animated fadeInUp');
	  } else {
	  	// Does nothing
	  }
	});
}

$('.join').css('visibility','hidden');
$('.join').on('inview', function(event, isInView) {
  if (isInView) {
      $(this).css('visibility','visible');
      $(this).addClass('animated fadeInUp');
  } else {
    // Does nothing
  }
});


// Inview Loading
$('#what').css('visibility','hidden');
$('#what').on('inview', function(event, isInView) {
  if (isInView) {
    $("#a_what").addClass('active');
    $(this).css('visibility','visible');
    $(this).addClass('animated fadeInUp')
  } else {
    $("#a_what").removeClass('active');
  }
});


$('#how').css('visibility','hidden');
$('#how').on('inview', function(event, isInView) {
  if (isInView) {
    $("#a_how").addClass('active');
    $(this).css('visibility','visible');
    $(this).addClass('animated fadeInUp');
  } else {
    $("#a_how").removeClass('active');
  }
});

$('#bin').css('visibility','hidden');
$('#bin').on('inview', function(event, isInView) {
  if (isInView) {
    $("#a_bin").addClass('active');
    $(this).css('visibility','visible');
    $(this).addClass('animated fadeInUp');
  } else {
    $("#a_bin").removeClass('active');
  }
});

$('#price').css('visibility','hidden');
$('#price').on('inview', function(event, isInView) {
  if (isInView) {
    $("#a_price").addClass('active');
    $(this).css('visibility','visible');
    $(this).addClass('animated fadeInUp');
  } else {
    $("#a_price").removeClass('active');
  }
});

$('#why').css('visibility','hidden');
$('#why').on('inview', function(event, isInView) {
  if (isInView) {
    $("#a_why").addClass('active');
    $(this).css('visibility','visible');
    $(this).addClass('animated fadeInUp');
  } else {
    $("#a_why").removeClass('active');
  }
});

$('#about').css('visibility','hidden');
$('#about').on('inview', function(event, isInView) {
  if (isInView) {
    $("#a_about").addClass('active');
    $(this).css('visibility','visible');
    $(this).addClass('animated fadeInUp');
  } else {
    $("#a_about").removeClass('active');
  }
});

$('#contact').css('visibility','hidden');
$('#contact').on('inview', function(event, isInView) {
  if (isInView) {
    $("#a_a_contact").addClass('active');
    $(this).css('visibility','visible');
  } else {
    $("#a_a_contact").removeClass('active');
  }
});