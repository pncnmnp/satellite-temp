import openaq
import pprint as pr
from math import ceil
import json

def make_request(date_from,date_to,limit):
    'limit means limit for no of entries in one page'
    date_from_text = '&date_from=' + date_from
    date_to_text =  '&date_to=' + date_to

    fileName = 'data_'+date_from+'to'+date_to+'.json'

    data_dic = {
        'country':'IN',
        'limit':limit,
        'date_to':date_to,
        'date_from':date_from,
        'parameter':['co'],
        'page':1
    }

    api = openaq.OpenAQ()
    status, resp = api.measurements(**data_dic)
    # df=api.measurements(**data_dic)

    data = resp['results']
    meta = resp['meta']

    no_of_entries = resp['meta']['found']

    with open('meta.json', "w") as write_file:
        json.dump(meta, write_file)

    no_of_pages= ceil( float(no_of_entries)/10000 )
    print(no_of_entries,no_of_pages,type(data))

    
    for i in range(no_of_pages-1):
        print( 'page:'+str(i+2)+'.......')
        page_no = i+2
        data_dic['page'] =page_no
        status, resp = api.measurements(**data_dic)
        data += resp['results']

    # with open( fileName,'w') as file:
    with open(fileName, "w") as write_file:
        json.dump(data, write_file)

    print('No of entries downloaded:',len(data))
    # print(resp)


make_request('2019-12-01','2019-12-31',10000)