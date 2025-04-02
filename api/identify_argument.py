import re

# 提取收藏的内容
def extract_favorite(sentence):
    patterns = [
        r"(?:我|最近|昨天|前天|刚才|刚刚|这几天|之前)?(?:收藏|钟爱|珍藏|保藏|保存)的?(\S+?)(?:的(?:电影|视频|歌曲|文章)|电影|视频|歌曲|文章)",
        r"(?:我|最近|昨天|前天|刚才|刚刚|这几天|之前)?(?:收藏|钟爱|珍藏|保藏|保存)的?(\S+?)的",
        r"(?:我|最近|昨天|前天|刚才|刚刚|这几天|之前)?(?:收藏|钟爱|珍藏|保藏|保存)的?(\S+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, sentence)
        if match:
            return match.group(1)
    return None

# 提取历史记录内容
def extract_history(sentence):
    patterns = [
        r"(?:已阅读的|回看已读过的|回看|已阅读)(\S+?)(?:的(?:视频|文章|报道|内容|攻略|指导|信息)|视频|文章|报道|内容|攻略|指导|信息)",
        r"(?:我(?:刚|已)?(?:看过|浏览|查看过|查看|阅读|回看|查阅)的?|用户(?:已|刚)?(?:看过|浏览|阅读|查看|查阅)的?|我的历史浏览中有关)(\S+?)(?:的(?:视频|文章|报道|内容|攻略|指导|信息)|视频|文章|报道|内容|攻略|指导|信息)",
        r"(?:回看|已(?:阅读|查看|浏览))(\S+?)(?:的(?:视频|文章|报道|内容|攻略|指导|信息)|视频|文章|报道|内容|攻略|指导|信息)",
    ]
    for pattern in patterns:
        match = re.search(pattern, sentence)
        if match:
            return match.group(1)
    return None

# 提取点赞或喜欢的内容
def extract_like(sentence):
    patterns = [
        r"(?:我(?:点赞的?|喜欢的?|的)?|点赞的?|喜欢的?)(\S+?)(?:的(?:视频|歌曲|电影|小说|评论|新闻)|视频|歌曲|电影|小说|评论|新闻)",
        r"(?:我(?:点赞的?|喜欢的?|的)?|点赞的?|喜欢的?)(\S+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, sentence)
        if match:
            return match.group(1)
    return None

# 提取最近看的小说历史
def extract_novel_history(sentence):
    patterns = [
        r"(?:我)?(?:最近|刚)?(?:看的|阅读的|痴迷的|拜读的|拜读|阅读|痴迷)?(\S+?)(?:的(?:小说|书)|小说|书)",
    ]
    for pattern in patterns:
        match = re.search(pattern, sentence)
        if match:
            return match.group(1)
    return None

# 提取用户名
def extract_username(sentence):
    pattern = r"(?:把|更新|修改|设置)?(?:我的)?用户名(?:改为|设置为|修改为|变更为|为)(\S+)"
    match = re.search(pattern, sentence)
    if match:
        return match.group(1)
    return None

# 提取昵称
def extract_nickname(sentence):
    pattern = r"(?:把|修改|设置)?(?:我的)?昵称(?:改为|设置为|修改为|变更为|为)(\S+)"
    match = re.search(pattern, sentence)
    if match:
        return match.group(1)
    return None

# 判断动作：打开或关闭
def identify_action(sentence):
    patterns_open = r"(?:打开|开启|启动|解锁|不要关闭|别关闭)(?:\S*)"
    patterns_close = r"(?:关闭|关|关掉|关上|不要打开|别打开)(?:\S*)"

    if re.search(patterns_open, sentence):
        if re.search(r"(不要打开|别打开)", sentence):
            return "关闭"
        return "打开"

    if re.search(patterns_close, sentence):
        if re.search(r"(不要关闭|别关闭)", sentence):
            return "打开"
        return "关闭"

    return None

# 主调用入口，根据 key 调用对应的方法
def process_input(key, sentence):
    functions = {
        "favorite": extract_favorite,
        "history": extract_history,
        "like": extract_like,
        "novel_history": extract_novel_history,
        "change_username": extract_username,
        "change_nickname": extract_nickname,
        "auto_backup": identify_action,
        "incognito_mode": identify_action,
        "night_mode": identify_action,
        "refresh_sound": identify_action,
        "notification": identify_action,
        "remend": identify_action
    }

    if key in functions:
        return functions[key](sentence)
    return None
