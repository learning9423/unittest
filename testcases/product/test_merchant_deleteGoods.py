import unittest
from pip._vendor import requests
from common.read_excel import ReadExcel
from common.send_request import SendRequest
from common.sql_data import SqlData

deleteGoods_data=ReadExcel().readExcel(r'../data/deleteGoods_api.xlsx','Sheet1')
s=requests.session()
class DeleteGoods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for i in range(len(deleteGoods_data)):
            if deleteGoods_data[i]['sql'] !='' and '{virtual_goods_id}' in deleteGoods_data[i]['body']:
                a=SqlData.themis_data(deleteGoods_data[i]['sql'])
                deleteGoods_data[i]['body']=deleteGoods_data[i]['body'].replace('{virtual_goods_id}',''.join('%s' %id for id in a[i]))
                if '{virtual_goods_id}' in deleteGoods_data[i]['msg']:#替换期望结果中的虚拟id
                    deleteGoods_data[i]['msg']=(deleteGoods_data[i]['msg'].replace('{virtual_goods_id}',''.join('%s' %id for id in a[i])))
            else:
                continue

    def test_deleteGoods1(self):
        '''商品id和token正确'''
        r=SendRequest.sendRequest(s,deleteGoods_data[0])
        expect_result = deleteGoods_data[0]['expect_result'].split(":",1)[1]
        msg = deleteGoods_data[0]['msg'].split(":",1)[1]

        self.assertEqual(r.json()['execute_status'], eval(expect_result), msg=r.json())
        self.assertEqual(r.json()['message'], eval(msg), msg=r.json())

    def test_deleteGoods2(self):
        '''商品id和token正确，商品在架'''
        r=SendRequest.sendRequest(s,deleteGoods_data[1])
        expect_result = deleteGoods_data[1]['expect_result'].split(":",1)[1]
        msg = deleteGoods_data[1]['msg'].split(":",1)[1]

        self.assertEqual(r.json()['execute_status'], eval(expect_result), msg=r.json())
        self.assertEqual(r.json()['message'], eval(msg), msg=r.json())

    def test_deleteGoods3(self):
        '''商品id为空,token正确'''
        r=SendRequest.sendRequest(s,deleteGoods_data[2])
        expect_result = deleteGoods_data[2]['expect_result'].split(":",1)[1]
        msg = deleteGoods_data[2]['msg'].split(":",1)[1]

        self.assertEqual(r.json()['execute_status'], eval(expect_result), msg=r.json())
        self.assertEqual(r.json()['message'], eval(msg), msg=r.json())

    def test_deleteGoods4(self):
        '''商品id正确，token错误'''
        r=SendRequest.sendRequest(s,deleteGoods_data[3])
        expect_result = deleteGoods_data[3]['expect_result'].split(":",1)[1]

        self.assertEqual(r.json(), eval(expect_result), msg=r.json())

    def test_deleteGoods5(self):
        '''商品id错误,token正确'''
        r=SendRequest.sendRequest(s,deleteGoods_data[4])
        expect_result = deleteGoods_data[4]['expect_result'].split(":",1)[1]
        msg = deleteGoods_data[4]['msg'].split(":",1)[1]

        self.assertEqual(r.json()['execute_status'], eval(expect_result), msg=r.json())
        self.assertEqual(r.json()['message'], eval(msg), msg=r.json())

if __name__ == '__main__':
    DeleteGoods().test_deleteGoods2()