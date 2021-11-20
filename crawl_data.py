covid_data_links = [#'https://vnexpress.net/microservice/sheet/type/vaccine_covid_19',
         'https://vnexpress.net/microservice/sheet/type/vaccine_data_vietnam_city',
         'https://vnexpress.net/microservice/sheet/type/vaccine_data_vietnam',
         'https://vnexpress.net/microservice/sheet/type/covid19_2021_281', # by day all province
         'https://vnexpress.net/microservice/sheet/type/covid19_2021_by_day',
         'https://vnexpress.net/microservice/sheet/type/covid19_2021_by_map',# by day general
         'https://covid19.who.int/WHO-COVID-19-global-table-data.csv',
         'https://covid19.who.int/WHO-COVID-19-global-data.csv']


import csv
import requests
import os

data_source_link = f"/content/drive/MyDrive/Data Engineering/data_csv"
for _covid_data_link in covid_data_links:
  CSV_URL = _covid_data_link
  with requests.Session() as s:
    download = s.get(CSV_URL)

    decoded_content = download.content.decode('utf-8')

    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    
    my_list = list(cr)
    if os.path.basename(_covid_data_link) == 'covid19_2021_281':
      my_list[1][0] = 'Tổng cộng'
    elif os.path.basename(_covid_data_link) == 'covid19_2021_by_map':
      my_list[0][20] = 'TỔNG TỬ VONG'
      my_list[0][21] = 'CÔNG BỐ HÔM QUA'
      my_list[0][22] = 'TỶ LỆ 1/100.000'
    file_name = os.path.join(data_source_link, os.path.basename(_covid_data_link))
    if '.csv' not in file_name:
      file_name = file_name + '.csv'
    with open(file_name, mode='w', encoding='utf-8') as employee_file:
      employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      for x in my_list:
        employee_writer.writerow(x)
    # for row in my_list[:5]:
    #   print(row)
    # print('\n')
