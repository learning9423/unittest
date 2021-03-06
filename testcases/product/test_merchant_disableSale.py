import unittest
from pip._vendor import requests
from common.read_excel import ReadExcel
from common.send_request import SendRequest
from common.sql_data import SqlData

disableSale_data= ReadExcel().readExcel(r'../data/ableSale&enableSale_api.xlsx', 'Sheet2')
s = requests.session()
class DisableSale(unittest.TestCase):
    '''商品下架'''
    @classmethod
    def setUpClass(cls):
        try:
            for i in range(len(disableSale_data)):
                if disableSale_data[i]['sql']!='' and '{virtual_goods_id}' in disableSale_data[i]['body']:
                    a=SqlData.themis_data(disableSale_data[i]['sql'])#连接数据库，返回数组，sql有可能不同
                    disableSale_data[i]['body']=disableSale_data[i]['body'].replace('{virtual_goods_id}',''.join('%s' %id for id in a[i]))
                else:
                    continue
        except IndexError:
                print('下标越界')#因为海外仓商品数量少，所以可能存在商品不足，赋值错误

    def test_disableSale1(self):
        '''有海外仓库存:直接下架'''
        r=SendRequest.sendRequest(s,disableSale_data[0])
        expect_result=disableSale_data[0]['expect_result'].split(":",1)[1]
        msg=disableSale_data[0]['msg'].split(":",1)[1]

        self.assertEqual(r.json()['execute_status'],eval(expect_result),msg=r.json())
        self.assertEqual(r.json()['data']['code'],eval(msg),msg=r.json())

    def test_disableSale2(self):
        '''有海外仓库存:清零标准仓库存不下架'''
        r=SendRequest.sendRequest(s,disableSale_data[1])
        expect_result=disableSale_data[1]['expect_result'].split(":",1)[1]
        msg=disableSale_data[1]['msg'].split(":",1)[1]

        self.assertEqual(r.json()['execute_status'],eval(expect_result),msg=r.json())
        self.assertEqual(r.json()['data']['code'],eval(msg),msg=r.json())

    def test_disableSale3(self):
        '''无海外仓直接下架:token和商品id都正确'''
        r=SendRequest.sendRequest(s,disableSale_data[2])
        expect_result=disableSale_data[2]['expect_result'].split(":",1)[1]
        msg=disableSale_data[2]['msg'].split(":",1)[1]

        self.assertEqual(r.json()['execute_status'],eval(expect_result),msg=r.json())
        self.assertEqual(r.json()['data']['code'],eval(msg),msg=r.json())

    def test_disableSale4(self):
        '''无海外仓直接下架:商品id错误'''
        r=SendRequest.sendRequest(s,disableSale_data[3])
        expect_result=disableSale_data[3]['expect_result'].split(":",1)[1]
        msg=disableSale_data[3]['msg'].split(":",1)[1]

        self.assertEqual(r.json()['execute_status'],eval(expect_result),msg=r.json())
        self.assertEqual(r.json()['data']['errors_list'][0]['code'], eval(msg),msg=r.json())
    def test_disableSale5(self):
        '''无海外仓库存直接下架:token错误'''
        r=SendRequest.sendRequest(s,disableSale_data[4])
        expect_result=disableSale_data[4]['expect_result'].split(":",1)[1]

        self.assertEqual(r.json(), eval(expect_result),msg=r.json())

if __name__ == '__main__':
    DisableSale().test_disableSale3()
