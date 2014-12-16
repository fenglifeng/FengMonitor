应用： sudo python main.py 即可

static文件夹里存放网页所需的js，css，image等文件

templates文件夹存放网页模板

inverter存放采集程序，以及数据库操作的程序。其中采集程序协议为modbus。如需修改可修改tcpserver.py中的收发程序。sip.py文件为采集数据格式。sqldb.py和operate.py为一系列的数据库操作，sqldb.py中的dbname可根据自己需求进行修改。test.db为sqlite数据库

config文件夹中存放网站的配置信息

code文件夹里为网站发布的具体代码