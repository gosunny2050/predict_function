说明：
app中经常有太多的功能，用户需要某个功能时候找不到或者花费很多时间才能找到，虽然ai的发展，可以给app创建一个ai功能，用户输入相关自然语言，自动帮忙用户定位到相关功能。例如：用户输入清理缓存，自动帮用户打开清理app缓存的功能

代码库主要分为三个部分：
api模块：主要提供匹配接口服务,里面的saved_bert_model 为训练生成的模型
generate_data: 主要生成训练数据
train_model: 主要是训练代码

请求样例:
curl --location --request POST 'http://xxx/predict/function' --header 'Host: xxx' --header 'Content-Type: application/json' --data '{ "message": "我收藏的周星驰的电影" }'

设计方案：

利用chatgpt生成训练数据集，基于bert-base-chinese基础模型，训练出来识别39个分类的模型 &结合mysql 全文索引相似度匹配进行匹配。
