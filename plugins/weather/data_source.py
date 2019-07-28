from config import HE_WEATHER_KEY
import requests

async def get_weather_of_city(location:str,api_type = 'forecast') -> str:

    #url ='https://free-api.heweather.com/v5/{}?city={}&key={}'
    #api_type:
    #now	    实况天气	    商业/免费
    #forecast	3-10天预报	    商业/免费
    #hourly	    逐小时预报	    商业/免费
    #lifestyle	生活指数	    商业/免费

    url = f'https://free-api.heweather.net/s6/weather/{api_type}?location={location}&key={HE_WEATHER_KEY}'
    data = requests.get(url).json()
    #获取失败 返回错误信息
    text = ''
    if data["HeWeather6"][0]["status"] != "ok":
        return "[ERROR]:("+data["HeWeather6"][0]["status"]+")-\n查询错误[CQ:at,qq=1325360514]"

    #DEBUG： print('\n\nSuccess\n')
    loc_time = data['HeWeather6'][0]['update']['loc']

    #获取成功
    if api_type == 'now':#实时天气
        print('\n\nNOW MODE\n')
        now = data['HeWeather6'][0]['now']

        fl = now['fl']#体感温度
        cond_txt = now['cond_txt']#天气状况描述
        wind_dir = now['wind_dir']#风向
        wind_spd = now['wind_spd']#风速 公里/小时
        pcpn = now['pcpn']#降雨量
        vis = now['vis']#能见度

        text =  """
            实时天气播报
            当地时间{}
            {}
            体感温度约{}°C
            {}，时速约{}公里
            降雨量为{}毫米
            能见度{}公里
            """.format(loc_time,cond_txt,fl,wind_dir,wind_spd,pcpn,vis)

    if api_type =='forecast':
        print('\n\nFORECAST MODE\n')
        forecase = data['HeWeather6'][0]['daily_forecast'][0]
        sr = forecase['sr']#日出时间
        tmp_max	= forecase['tmp_max']#最高温度
        tmp_min	= forecase['tmp_min']#最低温度
        cond_txt_d = forecase['cond_txt_d']#白天天气状况
        cond_txt_n = forecase['cond_txt_n']#夜晚~
        wind_dir = forecase['wind_dir']#风向
        wind_spd = forecase['wind_spd']#风速 公里/小时
        pop	= forecase['pop']#降水概率
        vis = forecase['vis']#能见度

        text =  """
            明日天气预报
            白天{},晚上{}
            温度大约在{}°C ~ {}°C之间
            {}日出
            {}风,时速{}公里
            降水概率为{}%
            能见度{}公里
                """.format(cond_txt_d,cond_txt_n,tmp_max,tmp_min,sr,wind_dir,wind_spd,pop,vis)

    if api_type =='hourly':
        print('\n\nHOURLY MODE')
        hourly = data['HeWeather6'][0]['hourly'][0]#未来一小时天气数据
        tmp = hourly['tmp']#温度
        cond_txt = hourly['cond_txt']#
        wind_dir = hourly['wind_dir']  # 风向
        wind_spd = hourly['wind_spd']  # 风速 公里/小时
        pop = hourly['pop']  # 降水概率
        vis = hourly['vis']  # 能见度

        text =  """
                未来一小时天气预报
                {}
                平均温度{}°C
                {}风 时速{}公里
                降水概率为{}%
                能见度{}公里
                """.format(cond_txt,tmp,wind_dir,wind_spd,pop,vis)

    if api_type == 'lifestyle':
        lifestyle = data['HeWeather6'][0]['lifestyle'][0]
        txt = lifestyle['txt']

        text =  txt

    if text == '':
        text = '''
                [ERROR]请确认是否正确查询
                查询方式    描述 
                forecast  预报明天天气(默认)
                now       实时天气
                hourly    未来一小时天气预报
                lifestyle 生活指数描述
                '''
    return text

