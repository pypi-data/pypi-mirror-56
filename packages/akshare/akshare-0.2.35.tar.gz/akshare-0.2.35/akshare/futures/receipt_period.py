# -*- coding:utf-8 -*-
# /usr/bin/env python
"""
Author: Albert King
date: 2019/10/25 12:10
contact: jindaxiang@163.com
desc: 获取交易法门-工具-仓单工具-仓单有效期
"""
import requests
import pandas as pd

from akshare.futures.cons import JYFM_TOOLS_RECEIPT_DATE_URL


def get_receipt_date():
    """
    获取期货仓单有效期数据
    :return: pd.DataFrame
            交易所    品种                                                到期日
    0   郑商所    普麦                                         9月的最后一个工作日
    1   郑商所    强麦                                         9月的最后一个工作日
    2   郑商所    粳稻              N年10月1日起注册的标准仓单，有效期至N+1年9月份最后一个工作日（含）
    3   郑商所    晚稻               每年10月1日起注册的标准仓单，应在次年9月份最后一个工作日之前全部注销
    4   郑商所    早稻             N年8月1日起注册，N+1年7月份最后一个工作日（含）上生产年度的可重新注册
    5   郑商所    玻璃               5月、11月第12个交易日（不含）之前注册的，当月的第15个交易日（含）
    6   郑商所    硅铁  每年 2 月、6 月、10 月第 12 个交易日（不含该日）之前注册的厂库和仓库标准仓单，应...
    7   郑商所    锰硅  每年 10 月第 12 个交易日（不含该日）之前注册的仓库标准仓单，应在当月的第 15 个交...
    8   郑商所   动力煤  每年5月、11月第7个交易日（不含）之前注册的标准仓单，应在当月的第10个交易日（含）之前全部注销
    9   郑商所    红枣  生产日期在11月1日之前的红枣不得在当年11月1日（含该日）之后注册。N年11月1日起接受红...
    10  郑商所    苹果  每年1月、5月、7月第12个交易日（不含该日）之前注册的厂库标准仓单，应在当月的第15个交易...
    11  郑商所    尿素  每年2月、6月、10月第12个交易日（不含该日）之前注册的厂库和仓库标准仓单，应在当月的第1...
    12  郑商所    甲醇               5月、11月第12个交易日（不含）之前注册的，当月的第15个交易日（含）
    13  郑商所   PTA  9月第12个交易日前（不含）注册的，第15个交易日（含）之前注销，第16个交易日（含）之后受...
    14  郑商所    菜油              N年6月1日起注册的菜油标准仓单有效期至N+1年5月份最后一个工作日（含）
    15  郑商所    菜粕  每年3月、7月、11月第12个交易日（不含）之前注册的标准仓单，应在当月的第15个交易日（含...
    16  郑商所    菜籽                 N年11月份最后一个工作日（含），N年6月1日起接受菜籽标准仓单注册
    17  郑商所    棉纱  每年2月、4月、6月、8月、10月、12月第12个交易日（不含该日）之前注册的厂库和仓库标准...
    18  郑商所    棉花                                      N+2年3月最后一个工作日
    19  郑商所    白糖  N制糖年度（每年的10月1日至次年的9月30日）生产的白糖所注册的标准仓单有效期为该制糖年度...
    20  大商所   苯乙烯                          每个交割月的最后交割日之前(含当日)必须进行注销。
    21  大商所   乙二醇                       每年3月最后一个交易日之前(含最后一个交易日)必须注销。
    22  大商所  聚氯乙烯                                          3月最后一个工作日
    23  大商所   聚丙烯                                          3月最后一个工作日
    24  大商所    塑料                                          3月最后一个工作日
    25  大商所    焦炭                                          3月最后一个工作日
    26  大商所    焦煤                                    每月最后交割日后3日内必须注销
    27  大商所   铁矿石                                          3月最后一个工作日
    28  大商所   胶合板                                     3、7、11月最后一个工作日
    29  大商所   纤维板                                     3、7、11月最后一个工作日
    30  大商所    粳米                       每个交割月份最后交割日前(含当日)应当进行标准仓单注销。
    31  大商所    鸡蛋                                 每月最后交割日后1个交易日内必须注销
    32  大商所    淀粉                                     3、7、11月最后一个工作日
    33  大商所    玉米                                          3月最后一个工作日
    34  大商所   棕榈油                                    每月最后交割日后3日内必须注销
    35  大商所    豆油                                          3月最后一个工作日
    36  大商所    豆粕                                     3、7、11月最后一个工作日
    37  大商所    豆二                                          3月最后一个工作日
    38  大商所    豆一                                          3月最后一个工作日
    39  上期所    纸浆  用于实物交割的国产漂针浆有效期限为生产年份的第二年的最后一个交割月份，超过期限的转作现货并注销。
    40  上期所   燃料油   燃料油保税标准仓单有效期限为保税标准仓单生效年份的第二年的最后一个交割月份，超过期限的转作现货。
    41  上期所  石油沥青  每年9月15日（遇法定假日顺延）之前生成的石油沥青厂库标准仓单，应在10月的最后一个工作日（...
    42  上期所  天然橡胶  国产天然橡胶（SCR WF）在库交割的有效期限为生产年份的第二年的最后一个交割月份（11月）...
    43  上期所    线材    每批商品的有效期限为生产日起的90天内，并且应在生产日起的30天内入指定交割仓库方可制作仓单。
    44  上期所  热轧卷板  热轧卷板期货的仓单有效期设定为标准仓单生产日期起的360天，每一仓单的热轧卷板以其中最早的生...
    45  上期所   螺纹钢    每批商品的有效期限为生产日起的90天内，并且应在生产日起的30天内入指定交割仓库方可制作仓单。
    46  上期所    白银                                               永久有效
    47  上期所    黄金                                               永久有效
    48  上期所   不锈钢  每批不锈钢应在生产日起的45天内入指定交割仓库，方可制作仓库标准仓单。每一仓单的不锈钢生产日...
    49  上期所     锡                                               永久有效
    50  上期所     镍                                               永久有效
    51  上期所     铅                                               永久有效
    52  上期所     铝                                               永久有效
    53  上期所     锌                                               永久有效
    54  上期所     铜                                               永久有效
    """
    res = requests.get(JYFM_TOOLS_RECEIPT_DATE_URL)
    receipt_dict = res.json()["data"]
    exchange_name_list = [item["exchangeName"] for item in receipt_dict]
    product_name_list = [item["productName"] for item in receipt_dict]
    expire_date_list = [item["expireDate"] for item in receipt_dict]
    return pd.DataFrame([exchange_name_list, product_name_list, expire_date_list], index=["交易所", "品种", "到期日"]).T


if __name__ == "__main__":
    df = get_receipt_date()
    print(df)
