from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import SKU
from goods.serializers import HotSKUListSerializer, GoodsListSerializer
from orders.models import OrderInfo, OrderGoods
from orders.serializers import ddanxlh, og, og2

"""
表的设计思想
    １．根据产品的原型，尽量多的分析标的字段(不要分析表和表质检的关系)
    ２．分析表和表之间的关系

"""

"""
热销数据和列表数据
热销数据应该是到哪个分类去，获取哪个分类的热销数据
１．获取分类ｉｄ
２．根据ｉｄ获取数据
３．将数据转化为字典(json数据)
４．返回响应

GET      /goods/categories/(?P<category_id>\d+)/hotskus/
"""
from rest_framework.generics import ListAPIView
class HotSKUListAPIView(ListAPIView):

    pagination_class = None

    def get_queryset(self):
        category_id = self.kwargs['category_id']

        return SKU.objects.filter(category_id=category_id).order_by('-sales')[:2]
        # http://127.0.0.1:8000/goods/categories/115/hotskus/

    serializer_class = HotSKUListSerializer

"""
当用户选择一个分类的时候,我们需要对分类数据进行 排序,进行分页处理

简化需求,一步一步的实现

先获取所有分类数据,再排序,再分页

先获取所有的分类数据
1.先获取所有数据  [SKU,SKU,SKU]
2.将对象列表转换位字典(JSON)
3. 返回相应

GET   /goods/categories/(?P<category_id>\d+)/skus/
"""
from rest_framework.filters import OrderingFilter

class SKUListAPIView(ListAPIView):

    # 通过定义过滤后端，来实行排序行为
    filter_backends = [OrderingFilter]
    ordering_fields = ['create_time','price','sales']

    serializer_class = HotSKUListSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return SKU.objects.filter(category_id=category_id)


# 　SKU搜索

from drf_haystack.viewsets import HaystackViewSet
from .serializers import SKUIndexSerializer

class SKUSearchViewSet(HaystackViewSet):
    index_models = [SKU]
    serializer_class = SKUIndexSerializer


# class GoodsListVPIView(ListAPIView):
#
#
#
#     def list(self, request, *args, **kwargs):
#         pass

class GoodsListAPIView(APIView):

    # 验证用户
    permission_classes = [IsAuthenticated]


    def get(self,request):
    # 获取用户信息
        user = request.user


    #　获取订单列表数据
        orderlist = OrderInfo.objects.filter(user_id=user.id)
        serializer = GoodsListSerializer(orderlist,many=True)

        return Response(serializer.data)
class GoodsCommentsAPIView(APIView):
    def get(self,request,goodsid):
        goodlist = OrderGoods.objects.filter(sku_id=int(goodsid))
        for good in goodlist:
            good.username = OrderInfo.objects.get(order_id=good.order_id).user.username
        s=og2(goodlist,many=True)
        return Response(s.data)