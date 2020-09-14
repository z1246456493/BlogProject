from django.db import models

# Create your models here.
class Alipay(models.Model):
    order_id=models.IntegerField('订单编号',primary_key=True)
    state_payment=models.CharField('支付状态',max_length=20)
    contract_status=models.CharField('签约状态',max_length=20)
    created_time=models.DateTimeField('订单创建时间',auto_now_add=True)
    updated_time=models.DateTimeField('订单修改时间',auto_now=True)
    # house_profile=models.OneToOneField(House,on_delete=models.CASCADE)
    # user_profile=models.ForeignKey(User,on_delete=models.CASCADE)

