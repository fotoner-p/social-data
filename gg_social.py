import pandas as pd
from social_crawler import request_company_list, request_company_info

open_url = "https://openapi.gg.go.kr/Pwnmsoctysevinst"

position_year = "2020"

cido = [
    {
      "SCLAS_NM": "서울특별시",
      "CTPRVN_CODE": "001"
    },
    {
      "SCLAS_NM": "부산광역시",
      "CTPRVN_CODE": "002"
    },
    {
      "SCLAS_NM": "대구광역시",
      "CTPRVN_CODE": "003"
    },
    {
      "SCLAS_NM": "인천광역시",
      "CTPRVN_CODE": "004"
    },
    {
      "SCLAS_NM": "대전광역시",
      "CTPRVN_CODE": "005"
    },
    {
      "SCLAS_NM": "광주광역시",
      "CTPRVN_CODE": "006"
    },
    {
      "SCLAS_NM": "울산광역시",
      "CTPRVN_CODE": "007"
    },
    {
      "SCLAS_NM": "경기도",
      "CTPRVN_CODE": "008"
    },
    {
      "SCLAS_NM": "강원도",
      "CTPRVN_CODE": "009"
    },
    {
      "SCLAS_NM": "충청북도",
      "CTPRVN_CODE": "010"
    },
    {
      "SCLAS_NM": "충청남도",
      "CTPRVN_CODE": "011"
    },
    {
      "SCLAS_NM": "경상북도",
      "CTPRVN_CODE": "012"
    },
    {
      "SCLAS_NM": "경상남도",
      "CTPRVN_CODE": "013"
    },
    {
      "SCLAS_NM": "전라남도",
      "CTPRVN_CODE": "014"
    },
    {
      "SCLAS_NM": "전라북도",
      "CTPRVN_CODE": "015"
    },
    {
      "SCLAS_NM": "제주특별자치도",
      "CTPRVN_CODE": "016"
    },
    {
      "SCLAS_NM": "세종특별자치시",
      "CTPRVN_CODE": "017"
    }
  ]

for item in cido:
    print(item['SCLAS_NM'] + " 수집중")

    ids = request_company_list(item["CTPRVN_CODE"])

    result_list = []
    for id in ids:
        print(id)
        try:
            result_list.append(request_company_info(id, position_year))

        except Exception:
            print("None")

    df = pd.DataFrame(result_list, columns=["업체명", "대표자명", "대표자 전화번호", "관리자명", "관리자 전화번호", "관리자 이메일", "주소", "상반기 서비스 건수", "상반기 제공인력", "하반기 서비스 건수", "하반기 제공인력"])
    df.to_csv(item['SCLAS_NM'] + "_리스트.csv", index=False, encoding="cp949")

    print()
