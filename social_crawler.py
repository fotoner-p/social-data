import requests
import re
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse, parse_qs


def request_raw(city, page):
    url = "https://www.socialservice.or.kr:444/user/svcsrch/supply/supplyList.do"

    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {
        'p_ctprvn': city,
        'pageIndex': page,
        'p_order': '01',
        'p_search': 'A',
        'p_ctprvn_code': city,
        'p_signgu_code': '',
        'p_intrstSvc': '3000',
        'p_orderby': '01'
    }
    req = requests.post(url, headers=headers, data=payload)

    return req


def request_company_list(city):
    cid_list = []

    req = request_raw(city, '1')
    soup = bs(req.text, 'html.parser')

    count_raw = soup.find('strong', 'colorOrange')
    print(count_raw.text)

    regex = re.compile("\d+")

    # 정규표현식에 의해 숫자만 가져옴
    size = int(regex.findall(count_raw.text)[0])

    count = 0
    page = 1
    while True:
        print(page, end=' ')
        req = request_raw(city, str(page))

        soup = bs(req.text, 'html.parser')
        company_list_raw = soup.find_all('tr', 'over')

        for raw in company_list_raw:
            if count == size:
                return cid_list

            url = urlparse(raw.find_all('a')[0].attrs['href'])
            parse = parse_qs(url.query)
            cid = parse['p_prinst_id'][0][1:]
            cid_list.append(cid)

            count += 1

        page += 1


def request_company_info(id_str):
    url = "https://www.socialservice.or.kr:444/user/svcsrch/supply/supplyView.do"

    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {
        'p_prinst_id': id_str,
        'p_bsns': '3000'
    }

    req = requests.post(url, headers=headers, data=payload)

    soup = bs(req.text, 'html.parser')
    section = soup.find_all("div", {'class': ['tbl03', 'mT0']})[0]

    title = section.select("table > thead > tr > th > strong")[0].text
    section = section.select("table > tbody")[0]

    ceo_name = section.select("tr:nth-of-type(1) > td:nth-of-type(1)")[0].text
    ceo_number = section.select("tr:nth-of-type(2) > td:nth-of-type(1)")[0].text

    admin_name = section.select("tr:nth-of-type(1) > td:nth-of-type(2)")[0].text
    admin_number = section.select("tr:nth-of-type(2) > td:nth-of-type(2)")[0].text
    if admin_number == '-':
        admin_number = ''

    admin_email = section.select("tr:nth-of-type(3) > td:nth-of-type(2)")[0].text

    address = section.select("tr:nth-of-type(5) > td")[0].text.replace("\xa0", " ")

    div = soup.find_all("div", "tbl03")
    h4 = soup.find_all("h4", "sub_title02")

    for i, item in enumerate(h4):
        if item.text.find("사업실적") == 0:
            user = div[i + 1].select("table > tbody > tr:nth-of-type(1) > td:nth-of-type(5)")[0].text
            provide = div[i + 1].select("table > tbody > tr:nth-of-type(1) > td:nth-of-type(6)")[0].text

            if user == '-':
                user = ''

            if provide == '-':
                provide = ''

            return [title, ceo_name, ceo_number, admin_name, admin_number, admin_email, address, user, provide]
            # 업체명, 대표자명, 대표자 전화번호, 관리자명, 관리자 전화번호, 관리자 이메일, 주소, 제공건수, 제공인력


if __name__ == "__main__":
    result = request_company_list('003')
