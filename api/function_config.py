function_config = {
    "0": {
        "function_name": "favorite",
        "argument_name": "query"
    },
    "1": {
        "function_name": "history",
        "argument_name": "query"
    },
    "2": {
        "function_name": "like",
        "argument_name": "query"
    },
    "3": {
        "function_name": "novel_bookshelf",
        "argument_name": ""
    },
    "4": {
        "function_name": "novel_history",
        "argument_name": "query"
    },
    "5": {
        "function_name": "member_center",
        "argument_name": ""
    },
    "6": {
        "function_name": "wallet",
        "argument_name": ""
    },
    "7": {
        "function_name": "coupon_package",
        "argument_name": ""
    },
    "8": {
        "function_name": "clear_cache",
        "argument_name": ""
    },
    "9": {
        "function_name": "publisher",
        "argument_name": ""
    },
    "10": {
        "function_name": "scan_code",
        "argument_name": ""
    },
    "11": {
        "function_name": "network_detection",
        "argument_name": ""
    },
    "12": {
        "function_name": "file_download",
        "argument_name": ""
    },
    "13": {
        "function_name": "auto_backup",
        "argument_name": "action"
    },
    "14": {
        "function_name": "recycle",
        "argument_name": ""
    },
    "15": {
        "function_name": "incognito_mode",
        "argument_name": "action"
    },
    "16": {
        "function_name": "night_mode",
        "argument_name": "action"
    },
    "17": {
        "function_name": "font_size",
        "argument_name": ""
    },
    "18": {
        "function_name": "homepage",
        "argument_name": ""
    },
    "19": {
        "function_name": "refresh_sound",
        "argument_name": "action"
    },
    "20": {
        "function_name": "notification",
        "argument_name": "action"
    },
    "21": {
        "function_name": "remend",
        "argument_name": "action"
    },
    "22": {
        "function_name": "identity_verification",
        "argument_name": ""
    },
    "23": {
        "function_name": "logout",
        "argument_name": ""
    },
    "24": {
        "function_name": "cancel_account",
        "argument_name": ""
    },
    "25": {
        "function_name": "change_password",
        "argument_name": ""
    },
    "26": {
        "function_name": "change_phone_number",
        "argument_name": ""
    },
    "27": {
        "function_name": "change_email",
        "argument_name": ""
    },
    "28": {
        "function_name": "change_username",
        "argument_name": "username"
    },
    "29": {
        "function_name": "change_nickname",
        "argument_name": "nickname"
    },
    "30": {
        "function_name": "change_profile_picture",
        "argument_name": ""
    },
    "31": {
        "function_name": "change_delivery_address",
        "argument_name": ""
    },
    "32": {
        "function_name": "duxiaoman",
        "argument_name": ""
    },
    "33": {
        "function_name": "music",
        "argument_name": ""
    },
    "34": {
        "function_name": "stock",
        "argument_name": ""
    },
    "35": {
        "function_name": "health",
        "argument_name": ""
    },
    "36": {
        "function_name": "netdisk",
        "argument_name": ""
    },
    "37": {
        "function_name": "anchor_center",
        "argument_name": ""
    },
    "38": {
        "function_name": "free_data",
        "argument_name": ""
    },
    "39": {
        "function_name": "unknow",
        "argument_name": ""
    }
}
# 根据索引获取函数信息的函数
def fetch_function_details(index):
    index_str = str(index)  # 将索引转换为字符串
    if index_str in function_config:
        return function_config[index_str]
    return {"function_name": "", "argument_name": ""}

# 示例：获取索引32的值
index = 32
result = fetch_function_details(index)
print(result)
