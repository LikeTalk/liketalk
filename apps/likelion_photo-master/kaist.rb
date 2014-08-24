
def kaist 

  teachers = [
  ["이태우", "KAIST 전산학과", "/members/kaist/t1.jpg", "Indentation Error"], #마지막에 쉼표 잊지 마시고
  ["김동우", "KAIST 전산학과", "/members/kaist/t2.jpg", "Syntax Error"] #여기도 마지막에 쉼표 잊지 마시고
  ].shuffle

  students = [
  ["정지혜", "한남대 경영정보학과", "/members/kaist/s1.jpg"],
  ["정용한", "KAIST 산업및시스템공학과", "/members/kaist/s2.jpg"],
  ["임재현", "KAIST 전기및전자공학과", "/members/kaist/s3.jpg"],
  ["이석민", "KAIST 수학과/경영공학과", "/members/kaist/s4.jpg"],
  ["한동식", "KAIST 바이오및뇌공학과", "/members/kaist/s5.jpg"],
  ["구아영", "충남대 회계학과", "/members/kaist/s6.jpg"],
  ["김현수", "KAIST 무학과", "/members/kaist/s7.jpg"],
  ["김동화", "KAIST 전기및전자공학과", "/members/kaist/s8.jpg"],
  ["강민지", "KAIST 산업디자인과", "/members/kaist/s9.jpg"],
  ["손현진", "KAIST 바이오및뇌공학과", "/members/kaist/s10.jpg"],
  ["유수형", "KAIST 건설및환경공학과", "/members/kaist/s11.jpg"]
  ].shuffle

  teachers + students
end

