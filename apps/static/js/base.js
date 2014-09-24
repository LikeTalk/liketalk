$(document).ready(function () {
    $('#cand1').click(function(){
    $.ajax({
      url = "/test",
      data = {
        roundnum : {{ player_game.game_round }},
        seasonnum : {{player_game.season_num}},
        cand1_selected = {{ player_game.candidate_A_namename }},
        cand2_selected = 0,
        cand1_count = {{ player_game.candidate_A_count }},
        cand2_count = 0,
      },
      dataType : 'JSON',
      success: function(data){
        $('#myround').text(data.roundnum)
        $('#Aphoto').attr('src',data.Aphotolink)
        $('#Bphoto').attr('src',data.Bphotolink)
        $('.candAname').text(data.Aname)
        $('.candBname').text(data.Bname)
        $('.candAschool').text(data.Aschool)
        $('.candBschool').text(data.Bschool)
      }
    })
  })

    $('#cand2').click(function(){
    $.ajax({
      url = "/test",
      data = {
        roundnum : {{ player_game.game_round }},
        seasonnum : {{player_game.season_num}},
        cand1_selected = 0 ,
        cand2_selected = {{ player_game.candidate_B_namename }},
        cand1_count = 0,
        cand2_count = {{ player_game.candidate_A_count }},
      },
      dataType : 'JSON',
      success: function(data){
        $('#myround').text(data.roundnum)
        $('#Aphoto').attr('src',data.Aphotolink)
        $('#Bphoto').attr('src',data.Bphotolink)
        $('.candAname').text(data.Aname)
        $('.candBname').text(data.Bname)
        $('.candAschool').text(data.Aschool)
        $('.candBschool').text(data.Bschool)
      }
    })
  })

});
