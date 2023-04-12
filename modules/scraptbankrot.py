import re
import requests
import statistics
from bs4 import BeautifulSoup


def extract_addr(cadastr=None):
    if cadastr is not None:
        url = f"https://api.egrnka.ru/api/cadnum/base-n/{cadastr}"
        response = requests.request("GET", url, )
        return response.json()['address']
    else:
        return "No address"


def extract_price_avito(region):
    URL_REG = f"https://www.avito.ru/web/1/slocations?q={region}"
    response_reg = requests.request("GET", URL_REG)
    regionid = response_reg.json()['result']['locations'][0]['parent']['id']
    URL_PARS = f"https://www.avito.ru/web/1/js/items?categoryId=26&locationId={regionid}"
    # print(URL_PARS)
    response_pars = requests.request("GET", URL_PARS)
    av_price_list = []

    for cat_item in response_pars.json()['catalog']['items']:
        # print(cat_item['priceDetailed']['value'])
        try:
            if cat_item['normalizedPrice'] is not None:
                format_price = cat_item['normalizedPrice']
                fq = (format_price.replace(u'\xa0', u' ')).split(" ")

                if len(fq) > 4:
                    final_av_price = int(f"{fq[0]}{fq[1]}")
                    av_price_list.append(final_av_price)
                else:
                    final_av_price = int(f"{fq[0]}")
                    av_price_list.append(final_av_price)

        except KeyError:
            pass

    return int(statistics.mean(av_price_list))


def extract_price_cian(region):
    regex = r"([A-Za-z0-9]+( [A-Za-z0-9]+)+)"
    URL_REG = f"https://www.cian.ru/cian-api/site/v1/search-regions-cities/?text={region}"
    response_reg = requests.request("GET", URL_REG)
    regionid = response_reg.json()['data']['items'][0]['id']
    URL_PARS = f"https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=3&offer_type=suburban" \
               f"&region={regionid}"
    response_pars = requests.request("GET", URL_PARS)
    soup = BeautifulSoup(response_pars.text, 'html.parser')
    all_soup = soup.findAll('div', class_="_93444fe79c--row--kEHOK")
    list_cia = []
    list_price = []

    for one_soup in all_soup:
        temp_list_cia = []
        try:
            temp_list_cia.append(one_soup.findNext('span', class_="").text)
        except AttributeError:
            pass
        list_cia.append(temp_list_cia)

    for i in range(len(list_cia)):
        for itemson in list_cia[i]:
            matches = re.findall(regex, itemson, re.MULTILINE)
            if not matches:
                pass
            else:
                matqqq = int((matches[0][0]).replace(" ", ""))
                list_price.append(int(matqqq // 2))

    # return list_price
    finish_price = statistics.mean(list_price)
    return int(finish_price)

def extract_price_yandex(region):
    URL_REG = f"https://realty.ya.ru/gate/react-suggest/region/?text={region}"
    response_reg = requests.request("GET", URL_REG)
    print(response_reg.text)
    # regionid = response_reg.json()['data']['items'][0]['id']
    # URL_PARS = f"https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&object_type%5B0%5D=3&offer_type=suburban" \
    #            f"&region={regionid}"
    # response_pars = requests.request("GET", URL_PARS)


def extract_tbankrot():
    number_page = 1
    cad_nem_reg = r"(([A-Za-z0-9]+(:[A-Za-z0-9]+)+)+)"
    square_reg = r"([0-9]*?)([,]?)([\s]?)([+]?)([/]?)([-]?)(\s?)([0-9]*?)([.]?)([0-9]\s?[0-9]*\s?)(кв. м|кв.м.)"

    URL = f"https://tbankrot.ru/?page={number_page}&swp=any_word&stop=%D0%B4%D0%BE%D0%BB%D1%8F%2C+%D0%B4%D0%BE%D0%BB%D0%B8&num" \
          "=&debtor_cat=0&debtor=&au=&org=&start_p1=&start_p2=&p1=&p2=&min_p1=&min_p2=&pp_1=&pp_2=&st_1=&st_2=&sz_1=&sz_2" \
          "=&ez_1=&ez_2=&et_1=&et_2=&parent_cat=2&sub_cat=5&sort_order=desc&sort=relevant&show_period=all&pattern_name" \
          "=&place%5B%5D=109&place%5B%5D=119&place%5B%5D=120&place%5B%5D=121&place%5B%5D=122&place%5B%5D=123&place%5B%5D" \
          "=124&place%5B%5D=125&place%5B%5D=126&place%5B%5D=127&place%5B%5D=128&place%5B%5D=129&place%5B%5D=131&place%5B" \
          "%5D=132&place%5B%5D=133&place%5B%5D=135&place%5B%5D=136&place%5B%5D=137&place%5B%5D=138&place%5B%5D=139&place" \
          "%5B%5D=140&place%5B%5D=141&place%5B%5D=142&place%5B%5D=145&place%5B%5D=146&place%5B%5D=149&place%5B%5D=151" \
          "&place%5B%5D=152&place%5B%5D=153&place%5B%5D=154&place%5B%5D=157&place%5B%5D=158&place%5B%5D=159&place%5B%5D" \
          "=160&place%5B%5D=161&place%5B%5D=162&place%5B%5D=165&place%5B%5D=166&place%5B%5D=168&place%5B%5D=170&place%5B" \
          "%5D=179&place%5B%5D=180&place%5B%5D=181&place%5B%5D=183&place%5B%5D=184&place%5B%5D=185&place%5B%5D=186&place" \
          "%5B%5D=187"

    headers = {
        'Cookie': '__ddg1_=U54VkYH9bjFrFT6NjroL; promo_rotation=5; tpABt=1; show_checked=; show_closed=; show_paused=; '
                  'only_photo=; has_org_answer=; toggle_block_1=visible; s_hash=cd13ea11cfce4fe9123d4636d5881333; '
                  '_ym_hash=0342ee562ce219e992e92aaec497f5e6; toggle_block_5=visible; timezone_=1; '
                  'key=0342ee562ce219e992e92aaec497f5e6; s360hash=0342ee562ce219e992e92aaec497f5e6; '
                  'date=2023-04-09+15%3A40%3A01; PHPSESSID=knskae3kvg0sur7jhp0eirvp45'
    }

    response = requests.request("GET", URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    all_soup = soup.findAll('div', 'torg')

    # print(all_soup)

    datas_list = []

    for one_soup in all_soup:
        temp_datas_list = []
        cadastral_number = one_soup.findNext('div', 'lot_text').text.split(
            "                                                        ")
        _price = one_soup.findNext('span', 'sum').text
        torg_price = (_price.split(",")[0]).replace(" ", "")

        try:
            cad_mat = re.findall(cad_nem_reg, cadastral_number[1], re.MULTILINE)
            sqe_mat = re.findall(square_reg, cadastral_number[1], re.MULTILINE)

            del_sqe_mat = ''.join(sqe_mat[0]).split('кв.м')
            del_op_mat = del_sqe_mat[0].split('+/-')

            if len(del_op_mat) == 2:
                final_sqe = int((float(del_op_mat[0]) - float(del_op_mat[1])))
            else:
                try:
                    final_sqe = int(del_op_mat[0])
                except ValueError:
                    scuk_sqe = del_op_mat[0].replace(' ', '')
                    final_sqe = int(scuk_sqe.split(",")[0])

            torg_price_100 = (int(torg_price) // final_sqe)

            for i in range(len(cad_mat)):
                try:
                    temp_datas_list.append(extract_addr(cad_mat[i][0]))
                except KeyError:
                    pass
                temp_datas_list.append(cad_mat[i][0])
                temp_datas_list.append(torg_price)
                temp_datas_list.append(torg_price_100)

            if temp_datas_list:
                datas_list.append(temp_datas_list)

        except IndexError:
            pass
    print(datas_list)

    # with open('data.json', 'w') as outfile:
    #     json.dump(datas_list, outfile, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    extract_price_yandex("Магадан")
    # extract_tbankrot()
    # extract_addr()
