

def ssu
  teachers = [
    ["김종찬", "숭실대 컴퓨터학부", "/members/ssu/t1.jpg", "Tech and Tech of Passion will change this world."], #마지막에 쉼표 잊지 마시고
    ["김진아", "단국대 컴퓨터학부", "/members/ssu/t2.jpg", "실행이 답이다"], #여기도 마지막에 쉼표 잊지 마시고
    ["황성현", "성균관대 소프트웨어학과", "/members/ssu/t3.jpg", "sunghyun.kitchen"] #마지막 element는 쉼표로 끝나지 않음
  ].shuffle

  students = [
    ["김영철", "성균관대 전자전기학과", "/members/ssu/s6.jpg"], 
    ["박진수", "숭실대 언론홍보학과", "/members/ssu/s8.jpg"], 
    ["장선옥", "중앙대 수학과", "/members/ssu/s4.jpg"],
    ["이지현", "숭실대 글로벌 미디어학과", "/members/ssu/s3.jpg"],
    ["신윤수", "숭실대 벤처중소기업학과", "/members/ssu/s10.jpg"], 
    ["임동균", "숭실대 벤처중소기업학과", "/members/ssu/s2.jpg"],
    ["김남윤", "동국대 경영정보학과", "/members/ssu/s5.jpg"],
    ["임태양", "중앙대 심리학과", "/members/ssu/s1.jpg"],
    ["박형규", "단국대 경영학과", "/members/ssu/s9.jpg"]
  ].shuffle

#선생님 셔플(랜덤) 한번 하고, 학생 셔플 한번 해서 넣음.
  teachers + students

end
