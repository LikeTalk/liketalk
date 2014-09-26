$(document).ready((function() {
    $('textarea').keydown(function(event) {
      // console.log('asdf');
        if (event.keyCode == 37 || event.keyCode == 39){
            event.preventDefault();

        }
        return false;
    });

    var block = false;
	$(window).keydown(function(e){
      if(block) return;
      // console.log($(this));  
      if (e.keyCode == 37){
        $('#matchup_img_1').click();
        block = true;
      }
      else if (e.keyCode == 39){
        $('#matchup_img_2').click();
        block = true;
      }
    });

	// 그룹사진 이펙트 효과 
	$("#A").mouseenter(function(){
    	$(this).css("opacity", 0.4);
    });
    
    $("#A").mouseleave(function(){
    	$(this).css("opacity", 1);
    });

    $("#B").mouseenter(function(){
    	$(this).css("opacity", 0.4);
    });
    
    $("#B").mouseleave(function(){
    	$(this).css("opacity", 1);
    });

    $("#C").mouseenter(function(){
    	$(this).css("opacity", 0.4);
    });
    
    $("#C").mouseleave(function(){
    	$(this).css("opacity", 1);
    });

    $("#D").mouseenter(function(){
    	$(this).css("opacity", 0.4);
    });
    
    $("#D").mouseleave(function(){
    	$(this).css("opacity", 1);
    });

    $("#E").mouseenter(function(){
    	$(this).css("opacity", 0.4);
    });
    
    $("#E").mouseleave(function(){
    	$(this).css("opacity", 1);
    });


	// 클릭하면 어두워짐 
	$("#matchup_img_1").click(function(){
    	$(this).css("opacity", 0.4);
    });

    $("#matchup_img_2").click(function(){
    	$(this).css("opacity", 0.4);
    });


	// 매치업 사진 마우스오버 이펙
 	$("#matchup_img_1").mouseenter(function(){
    	$(this).css("opacity", 0.4);
    	$(this).text("Click");
    });
    
    $("#matchup_img_1").mouseleave(function(){
    	$(this).css("opacity", 1);
    });

	$("#matchup_img_2").mouseenter(function(){
    	$(this).css("opacity", 0.4);
    });
    
    $("#matchup_img_2").mouseleave(function(){
    	$(this).css("opacity", 1);
    });







}))