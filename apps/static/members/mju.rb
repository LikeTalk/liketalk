
def mju

  teachers = [
    ["김상선", "명지대 컴퓨터공학과", "/members/mju/t1.jpg", "나는 수업중이다."], #마지막에 쉼표 잊지 마시고
    ["이상준", "명지대 컴퓨터공학과", "/members/mju/t2.jpg", "나도 수업중이다."], #여기도 마지막에 쉼표 잊지 마시고
    ["박세진", "명지대 컴퓨터공학과", "/members/mju/t3.jpg", "멋쟁이 사자로 만들어 드립니다."], #여기도 마지막에 쉼표 잊지 마시고
    ["신승수", "명지대 컴퓨터공학과", "/members/mju/t4.jpg", "제 글까지 보고있다니...심심하신가 봅니다."], #여기도 마지막에 쉼표 잊지 마시고
    ["최인용", "명지대 컴퓨터공학과", "/members/mju/t5.jpg", "Syntax Error"] #마지막 element는 쉼표로 끝나지 않음
  ].shuffle

  students = [
    ["박상현", "명지대 디지털미디어학과", "/members/mju/s1.jpg"], 
    ["정다은", "명지대 법학과", "/members/mju/s2.jpg"], 
    ["지현수", "명지대 디지털미디어학과", "/members/mju/s3.jpg"], 
    ["이유경", "명지대 경제학과", "/members/mju/s4.jpg"], 
    ["장미란", "명지대 경영학과", "/members/mju/s5.jpg"],
    ["김정연", "명지대 경영정보학과", "/members/mju/s6.jpg"], 
    ["김상현", "명지대 경영정보학과", "/members/mju/s7.jpg"],
    ["김용진", "명지대 경영정보학과", "/members/mju/s8.jpg"],
    ["윤  경", "명지대 컴퓨터공학과", "/members/mju/s9.jpg"],
    ["송민기", "명지대 디지털미디어학과", "/members/mju/s10.jpg"],
    ["조우정", "명지대 전공자유학부", "/members/mju/s11.jpg"],
    ["김경찬", "명지대 전공자유학부", "/members/mju/s12.jpg"],
    ["송수연", "명지대 전공자유학부", "/members/mju/s13.jpg"],
    ["신지원", "명지대 전공자유학부", "/members/mju/s14.jpg"],
    ["권미정", "안양대 영어영문학과", "/members/mju/s15.jpg"]
  ].shuffle

#선생님 셔플(랜덤) 한번 하고, 학생 셔플 한번 해서 넣음.
  teachers + students
end

