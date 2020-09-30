
import unittest
from pip._vendor import requests
from common.read_excel import ReadExcel
from common.send_request import SendRequest
from common.sql_data import SqlData


class AbleSale(unittest.TestCase):
    '''商品上架'''

    def __init__(self):
        # 数据初始化
        self.ableSale_data = ReadExcel().readExcel(r'../data/ableSale&enableSale_api.xlsx', 'Sheet1')
        for i in range(len(self.ableSale_data)):
            if self.ableSale_data[i]['sql']!='':
                a=SqlData.themis_data(self.ableSale_data[i]['sql'])
                self.ableSale_data[i]['body']=self.ableSale_data[i]['body'].replace('{virtual_goods_id}',''.join('%s' %id for id in a[i]))
            else:
                continue
        self.s = requests.session()
        self._type_equality_funcs={}

    def test_ableSale1(self):
        '''token和商品id都正确'''

        r=SendRequest.sendRequest(self.s,self.ableSale_data[0])
        expect_result=self.ableSale_data[0]['expect_result'].split(":")[1]
        msg=self.ableSale_data[0]['msg'].split(":")[1]

        self.assertEqual(r.json()['execute_status'],eval(expect_result),msg=r.json())
        self.assertEqual(r.json()['data']['code'],eval(msg),msg=r.json())

    def test_ableSale2(self):
        '''商品id错误'''
        #现接口返回错误，等开发修改
        r=SendRequest.sendRequest(self.s,self.ableSale_data[1])
        expect_result=self.ableSale_data[1]['expect_result'].split(":")[1]
        msg=self.ableSale_data[1]['msg'].split(":")[1]

        self.assertEqual(r.json()['execute_status'],eval(expect_result),msg=r.json())
        self.assertEqual(r.json()['data']['errors_list'][0]['code'], eval(msg),msg=r.json())

    def test_ableSale3(self):
        '''token错误'''
        r=SendRequest.sendRequest(self.s,self.ableSale_data[2])
        expect_result=self.ableSale_data[2]['expect_result'].split(":")[1]

        self.assertEqual(r.json(), eval(expect_result),msg=r.json())

if __name__ == '__main__':
    AbleSale().test_ableSale3()