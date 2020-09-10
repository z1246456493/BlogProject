import json
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.views import View
from django.conf import settings
from alipay import AliPay

# Create your views here.
# 部署时更改配置文件中Alipay，静态文件中key_file
app_private_key_string=open(settings.ALIPAY_KEY_DIR+'app_private_key.pem').read()
alipay_public_key_string=open(settings.ALIPAY_KEY_DIR+'alipay_public_key.pem').read()

ORDER_STATUAS=1

class MyAlipay(View):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.alipay=AliPay(
            appid=settings.ALIPAY_APP_ID,
            app_notify_url=None,
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type='RSA2',
            debug=True
        )
    def get_teade_url(self,oeder_id,amount):
        base_url='https://openapi.alipaydev.com/gateway.do'
        oeder_string=self.alipay.api_alipay_trade_page_pay(
            out_trade_no=oeder_id,
            total_amount=amount,
            subject=oeder_id,
            return_url=settings.ALIPAY_RETURN_URL,
            notify_url=settings.ALIPAY_NOTIFY_URL,
        )
        return base_url+'?'+oeder_string


    def get_trade_result(self,order_id):
        result=self.alipay.api_alipay_trade_query(out_trade_no=order_id)
        if result.get('trade_status')=='TRADE_SUCCESS':
            return True
        return False
    def get_veify_result(self,data,sign):
        return self.alipay.verify(data,sign)

class JumpView(MyAlipay):
    def get(self,request):
        return render(request,'ajax_alipay.html')

    def post(self,request):
        json_obj=json.loads(request.body)
        order_id=json_obj['order_id']
        money=json_obj['money']
        pay_url=self.get_teade_url(order_id,money)
        return JsonResponse({'pay_url':pay_url})

class ResultView(MyAlipay):
    def get(self,request):
        request_data={k:request.GET[K] for k in request.GET.keys()}
        print(request_data)
        order_id=request_data['out_trade_no']
        if ORDER_STATUAS==1:
            result=self.get_trade_result(order_id)
            if result:
                return HttpResponse('主动查询支付成功')
            else:
                return HttpResponse('支付失败')

    def post(self,request):
        request_data={k:request.GET[K] for k in request.GET.keys()}
        sign=request_data.pop['sign']
        is_verify=self.get_veify_result(request_data,sign)
        if is_verify:
            trade_status=request_data['trade_status']
            if trade_status=='TRADE_SUCCESS':
                return HttpResponse('ok')
            else:
                return HttpResponse('error')