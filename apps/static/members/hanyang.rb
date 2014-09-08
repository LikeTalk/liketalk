

def hanyang

  teachers = [
    ["고윤용", "한양대 컴퓨터공학부", "/members/hanyang/t1.jpg", "프로 알콜러"],
    ["이희원", "한양대 컴퓨터공학부", "/members/hanyang/t2.jpg", "프로 인디게이머"]
  ].shuffle

  students = [
    ["공다은", "한양대 문화인류학과", "/members/hanyang/s1.jpg"], 
    ["김도희", "한양대 경영학부", "/members/hanyang/s2.jpg"], 
    ["김동률", "한양대 융합전자공학부", "/members/hanyang/s3.jpg"], 
    ["김슬기", "한양대 피아노과", "/members/hanyang/s4.jpg"], 
    ["김지효", "한양대 무용학과", "/members/hanyang/s5.jpg"],
    ["서정암", "한양대 경영학부", "/members/hanyang/s6.jpg"], 
    ["성준석", "한양대 융합전자공학부", "/members/hanyang/s7.jpg"],
    ["신종영", "한양대 교육공학과", "/members/hanyang/s8.jpg"],
    ["이소영", "한양대 문화콘텐츠학과", "/members/hanyang/s9.jpg"],
    ["장래민", "한양대 경영학부", "/members/hanyang/s10.jpg"],
    ["정승호", "한양대 산업디자인학과", "/members/hanyang/s11.jpg"],
    ["정호건", "한양대 건축학과", "/members/hanyang/s12.jpg"]
  ].shuffle

#선생님 셔플(랜덤) 한번 하고, 학생 셔플 한번 해서 넣음.
  teachers + students

end
