function populateList() {
    var list = $("#follower-list");
    var group_id = list.attr('group_id');
    $.get("/linterest/get_group_slide_followers/" + group_id)
      .done(function(data) {
          var caption_list = $(".caption");
          // console.log('follower num: ' + data.followers.length);
          // console.log('member num ' + data.members.length);
          for (var i = 0; i < data.followers.length; i++) {
              var follower = data.followers[i];
              var new_follower = $(follower.html);

              new_follower.find('path').attr('id', 'cd-morphing-path-' + (i + 1));
              new_follower.find('clipPath').attr('id', 'cd-image-' + (i + 1));
              new_follower.find('image').attr('clip-path', 'url(#cd-image-' + (i + 1) + ')');
              new_follower.find('use').attr('xlink:href', '#cd-morphing-path-' + (i + 1));
              list.append(new_follower);
              var isMember = false;
              // judge whether current follower in the member list
              for (var j =0; j < data.members.length; j++) {
                  var currMemberName = data.members[j].username;
                  if (follower.username == currMemberName) {
                      console.log(follower.username + 'in the member list');
                      var isMember = true;

                  }
              }
              // console.log(follower.username + isMember);
              var new_caption = $(follower.caption_html);
              var member_caption = $(follower.member_caption_html);
              // append different caption html between followers and members
              if (isMember == true) {
                  caption_list.append(member_caption);
              } else {
                  caption_list.append(new_caption);
              }
          }
          var lis = list.children('li');
          var cap_lis = caption_list.children('li');
          lis.eq(0).attr('class', 'selected');
          cap_lis.eq(0).attr('class', 'selected');
          lis.eq(0).find('path').attr('d', 'M780,0H20C8.954,0,0,8.954,0,20v760c0,11.046,8.954,20,20,20h760c11.046,0,20-8.954,20-20V20 C800,8.954,791.046,0,780,0z');
          if (lis.length > 1) {
            lis.eq(1).attr('class', 'right');
            cap_lis.eq(1).attr('class', 'right');
          }
          manipulateList();
      });
}

// this function is to accept group followers
function likeBack(username){
    var group_id = $('.gallery').attr('group_id');
    console.log("accept " + username + " into group " + group_id);
    // save the user to the memeber list of the current
    $.post("/linterest/accept/" + username + "/" + group_id, {})
      .done(function(data) {
		  console.log('accept successfully');
          window.location.replace("/linterest/group_recommendations/" + group_id);
      });
}

function manipulateList() {
    var duration = ( $('.no-csstransitions').length > 0 ) ? 0 : 300;
	//define a svgClippedSlider object
	function svgClippedSlider(element) {
		this.element = element;
		this.slidesGallery = this.element.find('.gallery').children('li');
		this.slidesCaption = this.element.find('.caption').children('li');
		this.slidesNumber = this.slidesGallery.length;
		this.selectedSlide = this.slidesGallery.filter('.selected').index();
		this.arrowNext = this.element.find('.navigation').find('.next');
		this.arrowPrev = this.element.find('.navigation').find('.prev');

		this.visibleSlidePath = this.element.data('selected');
		this.lateralSlidePath = this.element.data('lateral');

		this.bindEvents();
	}

	svgClippedSlider.prototype.bindEvents = function() {
		var self = this;
		//detect click on one of the slides
		this.slidesGallery.on('click', function(event){
			if( !$(this).hasClass('selected') ) {
				//determine new slide index and show it
				var newSlideIndex = ( $(this).hasClass('left') )
					? self.showPrevSlide(self.selectedSlide - 1)
					: self.showNextSlide(self.selectedSlide + 1);
			}
		});
	}

	svgClippedSlider.prototype.showPrevSlide = function(index) {
		var self = this;
		this.selectedSlide = index;
		this.slidesGallery.eq(index + 1).add(this.slidesCaption.eq(index + 1)).removeClass('selected').addClass('right');
		this.slidesGallery.eq(index).add(this.slidesCaption.eq(index)).removeClass('left').addClass('selected');

		//morph the svg cliph path to reveal a different region of the image
		Snap("#cd-morphing-path-"+(index+1)).animate({'d': self.visibleSlidePath}, duration, mina.easeinout);
		Snap("#cd-morphing-path-"+(index+2)).animate({'d': self.lateralSlidePath}, duration, mina.easeinout);

		if( index - 1 >= 0  ) this.slidesGallery.eq(index - 1).add(this.slidesCaption.eq(index - 1)).removeClass('left-hide').addClass('left');
		if( index + 2 < this.slidesNumber ) this.slidesGallery.eq(index + 2).add(this.slidesCaption.eq(index + 2)).removeClass('right');

		( index <= 0 ) && this.element.addClass('prev-hidden');
		this.element.removeClass('next-hidden');

		//animate prev arrow on click
		this.arrowPrev.addClass('active').on('webkitAnimationEnd oanimationend msAnimationEnd animationend', function(){
			self.arrowPrev.removeClass('active');
		});
	}

	svgClippedSlider.prototype.showNextSlide = function(index) {
		var self = this;
		this.selectedSlide = index;
		this.slidesGallery.eq(index - 1).add(this.slidesCaption.eq(index - 1)).removeClass('selected').addClass('left');
		this.slidesGallery.eq(index).add(this.slidesCaption.eq(index)).removeClass('right').addClass('selected');

		//morph the svg cliph path to reveal a different region of the image
		Snap("#cd-morphing-path-"+(index+1)).animate({'d': self.visibleSlidePath}, duration, mina.easeinout);
		Snap("#cd-morphing-path-"+(index)).animate({'d': self.lateralSlidePath}, duration, mina.easeinout);

		if( index - 2 >= 0  ) this.slidesGallery.eq(index - 2).add(this.slidesCaption.eq(index - 2)).removeClass('left').addClass('left-hide');
		if( index + 1 < this.slidesNumber ) this.slidesGallery.eq(index + 1).add(this.slidesCaption.eq(index + 1)).addClass('right');

		( index + 1 >= this.slidesNumber ) && this.element.addClass('next-hidden');
		this.element.removeClass('prev-hidden');

		//animate next arrow on click
		this.arrowNext.addClass('active').on('webkitAnimationEnd oanimationend msAnimationEnd animationend', function(){
			self.arrowNext.removeClass('active');
		});
	}

	$('.cd-svg-clipped-slider').each(function(){
		//create a svgClippedSlider object for each .cd-svg-clipped-slider
		new svgClippedSlider($(this));
	});
}


$(document).ready(function () {
  // Add event-handlers
  populateList();


  // CSRF set-up copied from Django docs
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
});

