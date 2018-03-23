function getToDivision(divID) {
	var isSmoothScrollSupported = 'scrollBehavior' in document.documentElement.style;

	var ele = document.getElementById(divID);
	var distance = 0;
	while(ele){
	   distance += ele.offsetTop;
	   ele = ele.offsetParent;
	}
	distance=distance-30;

	var options = {
    "behavior": "smooth",
    "left": 0,
    "top": distance
	};

	if (isSmoothScrollSupported) {
	    window.scrollTo(options);
	}
	else {
    	var current=document.getElementById("body").scrollTop;
	    var difference=distance-current;
	    
	    var num=current;
	    if(difference >= 0) {
	    	var intr = setInterval(function(){
	    		window.scrollBy(0,5);
	    		num+=5;
	    		if(num>distance) clearInterval(intr);
	    	}, 0.5);
	    }
	    else {
	    	var num=current;
	    	var intr = setInterval(function(){
	    		window.scrollBy(0,-5);
	    		num-=5;
	    		if(num<distance) clearInterval(intr);
	    	}, 0.5);
	    }
	}
}