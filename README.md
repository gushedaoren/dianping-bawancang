本程序用于自动进行大众点评霸王餐点击，建议使用大众点评vip账户，普通账户参加霸王餐的有限


执行霸王餐程序
/usr/bin/python3 /var/www/dianping/bawangcan.py


设置定时任务：
contab -e


每天十点自动执行霸王餐任务

0 10 * * * /usr/bin/python3 /var/www/dianping/bawangcan.py > /var/log//dianping/bawangcan_logs_$(date).log 2>&1


每天十点半自动参加美丽变漂亮活动
30 10 * * * /usr/bin/python3 /var/www/dianping/beauty.py > /var/log/dianping/beauty_logs_$(date).log 2>&1


:wq退出成功设置定时任务



