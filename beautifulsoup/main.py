import Collector
# serialNumnCollector = Collector.SerialNumberCollector()
# serialset = serialNumnCollector.findOuter()
# print('已完成全部serialNumber的爬蟲')
# for n in serialset:
#     if len(n) < 5:
#         continue
#     goodsInfoCollector = Collector.GoodsInfoCollector(n)
#     goodsInfoCollector.search()
goodsInfoCollector = Collector.GoodsInfoCollector('433245')
goodsInfoCollector.search()
