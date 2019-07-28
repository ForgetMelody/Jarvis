from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand

from .API import *



@on_command('music', aliases=('点歌'),only_to_me=False)
async def weather(session: CommandSession):
    music = session.get('music', prompt='告诉我你想听的歌，sir')
    searcher = search()
    id = searcher.get_song_id(music)
    reply = f'[CQ:music,type=163,id={id}]'
    await session.send(reply)


@weather.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['music'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('歌名不能为空请重新输入')

    session.state[session.current_key] = stripped_arg


# on_natural_language 装饰器将函数声明为一个自然语言处理器
# keywords 表示需要响应的关键词，类型为任意可迭代对象，元素类型为 str
# 如果不传入 keywords，则响应所有没有被当作命令处理的消息
@on_natural_language(keywords={'来首'},only_to_me=False)
async def _(session: NLPSession):
    # 去掉消息首尾的空白符
    stripped_msg = session.msg_text.strip()
    if stripped_msg.startswith('来首'):
        music = stripped_msg[2:]

    if music == '群歌':
        music = '你渴望学习吗'
    if music == '国歌':
        music == '义勇军进行曲'

    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(90.0, 'music', current_arg=music or '')