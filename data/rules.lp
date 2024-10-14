% 利润损益报告的规则
goal(X, profit_loss_report) :- _goal(X, goal_1).
start_date(X, Y1, date) :- goal(X, profit_loss_report), _report_period(X, (Y1, Y2)).
end_date(X, Y2, date) :- goal(X, profit_loss_report), _report_period(X, (Y1, Y2)).

% 联系的规则
goal(X, contact) :- _goal(X, goal_4).
contact_topic(X, Y, string) :- goal(X, contact), _contact_topic(X, Y).
contact_channel(X, Y, string) :- goal(X, contact), _contact_channel(X, Y), Y == "phone".
contact_channel(X, Y, string) :- goal(X, contact), _contact_channel(X, Y), Y == "chat".
contact_channel(X, Y, string) :- goal(X, contact), _contact_channel(X, Y), Y == "video".