#!/usr/bin/env python3.7
#网络项目
from pyecharts import options as opts
from pyecharts.charts import Page, Radar
def network_score(candidate_name, proj_s, tec_s, prof_s, mg_s, com_s):
    """
proj_s 项目得分 共 30, 
tec_s 技术栈得分 共 25,  
prof_s 业务能力得分 共25, 
mg_s 管理能力得分 共10, 
com_s  沟通能力得分 共10

candidate_name 候选者姓名 "赵峻"

    """
    total_score= proj_s + tec_s + prof_s + mg_s + com_s
    print(total_score)



    v1 = [[proj_s, tec_s,  prof_s,  mg_s, com_s]]
#v1 候选人得分
    v2 = [[15, 12.5,  12.5,  5,  5]]
#v2 均线



    c = (
        Radar()
        .add_schema(
            schema=[
                opts.RadarIndicatorItem(name="项目", max_=30),
                opts.RadarIndicatorItem(name="技术栈", max_=25),
                opts.RadarIndicatorItem(name="业务能力", max_=25),
                
                opts.RadarIndicatorItem(name="管理", max_=10),
                opts.RadarIndicatorItem(name="沟通与逻辑", max_=10),
            ]
        )
        .add("候选人:{}".format(candidate_name) , v1,color="#b3e4a1",areastyle_opts=0.3)
        .add("均线", v2,color="#f9713c")
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="候选人:{} total:{}".format(candidate_name, total_score)))
        
        
    )
    c.render(candidate_name + ".html")

if __name__ == "__main__":
   pass
