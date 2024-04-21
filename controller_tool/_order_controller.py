import json
import requests

class OrderController:
    def __init__(self, controller) -> None:
        self.controller = controller

    def _fetch_hashkey(self, data):
        path = "uapi/hashkey"
        url = f"{self.controller.base_url}/{path}"
        headers = {
            "content-type": "application/json",
            "appKey": self.controller.api_key,
            "appSecret": self.controller.api_secret,
            "User-Agent": "Mozilla/5.0",
        }
        resp = requests.post(url, headers=headers, data=json.dumps(data))
        haskkey = resp.json()["HASH"]
        return haskkey

    def make_market_buy_order(self, stock_code, quantity):
        path = "uapi/domestic-stock/v1/trading/order-cash"
        url = f"{self.controller.base_url}/{path}"

        data = {
            "CANO": self.controller.acc_no_prefix,
            "ACNT_PRDT_CD": self.controller.acc_no_postfix,
            "PDNO": stock_code,
            "ORD_DVSN": "01",  # 시장가 거래
            "ORD_QTY": str(quantity),
            "ORD_UNPR": "0",  # 시장가 거래
        }
        hashkey = self._fetch_hashkey(data)

        headers = {
            "content-type": "application/json",
            "authorization": self.controller.access_token,
            "appKey": self.controller.api_key,
            "appSecret": self.controller.api_secret,
            "tr_id": "TTTC0802U",  # buy
            "custtype": "P",
            "hashkey": hashkey,
        }
        resp = requests.post(url, headers=headers, data=json.dumps(data))
        resp_data = resp.json()
        resp_data["meta"] = {"stock_code": stock_code, "quantity": quantity}
        return resp_data

    def make_market_sell_order(self, stock_code, quantity):
        path = "uapi/domestic-stock/v1/trading/order-cash"
        url = f"{self.controller.base_url}/{path}"

        data = {
            "CANO": self.controller.acc_no_prefix,
            "ACNT_PRDT_CD": self.controller.acc_no_postfix,
            "PDNO": stock_code,
            "ORD_DVSN": "01",  # 시장가 거래
            "ORD_QTY": str(quantity),
            "ORD_UNPR": "0",  # 시장가 거래
        }
        hashkey = self._fetch_hashkey(data)

        headers = {
            "content-type": "application/json",
            "authorization": self.controller.access_token,
            "appKey": self.controller.api_key,
            "appSecret": self.controller.api_secret,
            "tr_id": "TTTC0801U",  # sell
            "custtype": "P",
            "hashkey": hashkey,
        }
        resp = requests.post(url, headers=headers, data=json.dumps(data))
        resp_data = resp.json()
        resp_data["meta"] = {"stock_code": stock_code, "quantity": quantity}
        return resp_data
