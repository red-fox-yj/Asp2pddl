% 给定的事实
_goal(x, goal_1).  % 实体 x 的目标是 goal_1 (利润损益报告)
_report_period(x, ("01/01/2024", "03/31/2024")).  % 实体 x 的报告周期为 2024年1月1日到2024年3月31日
_goal(y, goal_4).  % 实体 y 的目标是 goal_4 (联系)
_contact_topic(y, x).  % 实体 y 联系的主题是 x
_contact_channel(y, "phone").  % 实体 y 的联系渠道是电话
