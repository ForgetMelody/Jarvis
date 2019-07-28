from nonebot import on_notice,on_request, NoticeSession,RequestSession


# 将函数注册为群成员增加通知处理器
@on_notice('group_increase')
async def _(session: NoticeSession):
    # 发送欢迎消息
    await session.send('欢迎新人')

@on_request('friend')
async  def _(session:RequestSession):
    await session.reject('Jarvis隶属于[1325360514]')


# 将函数注册为群请求处理器
@on_request('group')
async def _(session: RequestSession):

    # 验证信息正确，同意入群
    await session.approve()
