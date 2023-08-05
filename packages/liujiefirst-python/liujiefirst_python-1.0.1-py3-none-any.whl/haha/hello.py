# coding:UTF-8
# infos = ["新八叽", "神乐", "银时","桂", "小猿", "月咏", "小玉", "九"]
# name = "神乐"
# if name in infos:
    # print("该数据存在于列表之中！！！")
# else:
    # print("该数据不存在于列表之中！！！")

# infos = ["新八叽", "神乐", "银时","桂", "小猿", "月咏", "小玉", "九"]
# if "神乐" in infos:
    # print(infos.remove("神乐"))
    # print(infos.pop(1))
    
# print("(‘你好’)的数据类型： %s，('你好',)的数据类型： %s" % (type(("你好")), type(("你好",))))   
    
# infos = ("新八叽", "神乐", "银时","桂", "小猿", "月咏", "小玉", "九")
# name = "Bob"
# age = 20
# sex = "男"
# print("你好我是{}，今年{}岁，{}".format(name, age, sex))  


# print("{:0>4}".format(100000))
# print("{:a}".format(100))

# print("{:b}".format(10))
# print("{:d}".format(10))
# print("{:o}".format(10))
# print("{:x}".format(10))

# str1 = "   hello world"
# print(str1.center(20))  # 就是在字符串的两边填充空格
# print(str1.find("w"))   # 判断字符串中是否包含某个子字符串，和in类似，但是在包含这个子字符串的情况下，find 能返回
# print(str1.find("0"),3,5) # 这个子字符串所在的索引位置，如果不包含，那就会返回 -1,后面还可以使用参数来限制在指定的索引范围内查找
# print(str1.upper())
# print(str1.lower())
# print(str1.capitalize())#首字母大写，但是如果首字母是空格，则该函数无效

# # join 和 split 可以看成是列表和字符串之间的相互转换
# list = ["新八几", "银时", "神乐"]
# print("_".join(list))
# str = "新八几_银时_神乐"
# print(str.split("_", 1))    # 参数1代表拆分出的列表最大索引值
# date = "2019-09-26 14:09:00"
# result = date.split(" ")
# print("当前日期为： %s" % result[0].split("-"))
# print("当前时间为： %s" % result[1].split(":"))

# str = "hello world, hello liujie"
# result = str.replace(" ", "", 1) # 1代表替换的次数，只会替换一次，上面的字符串中出现了两次hello，只会替换第一次出现的
# print(result) 


# str1 = "www.baidu.com;\twww.csdn.cn;"
# mt1 = str1.maketrans(".", "_", ";")
# print(str1.translate(mt1))

# dict1 = dict([["hello", "world"]])
# dict2 = dict(hello = "world")
# print(dict1)
# print(dict2)

# dict2 = dict(hello = "world")
# if "hello" in dict2:
    # print("dict2 中存在与name对应的value：{}".format(dict2["hello"]))


# dict = dict(name="liujie", age=21, score=80)
# print("第一种方式：")
# for key in dict:
    # print("{}={}".format(key, dict[key]))
    
# print("第二种方式：使用items()函数")
# for key,value in dict.items():
    # print("{}={}".format(key, value))


# infos = ["新八叽", "神乐", "银时","桂", "小猿", "月咏", "小玉", "九"]
# if "神乐" in infos:
    # print(infos.remove("神乐"))
    # print(infos.pop(1))   
    # print(infos)

# dict = dict(name="liujie", age=21, score=80)
# print("获取存在的key：{}".format(dict.get("name")))
# print("获取不存在的key：{}".format(dict.get("hello")))
# print("获取不存在的key且有设置默认值：{}".format(dict.get("hello","字典中不存在该key！！！")))
# print(type(dict.values()))
# print(dict.values())
# print(type(dict.keys()))
# print(dict.keys())


# dict1 = dict.fromkeys(("key1", "key2"),"value")
# dict2 = dict.fromkeys("hello", 100)
# print(dict1)
# print(dict2)

# dict = dict(name="liujie", age=21, score=80)
# print(type(dict.values()))
# print(dict.values())
# print(type(dict.keys()))
# print(dict.keys())

# def fun1():
    # return "this is the first function!!!"
# print(type(fun1))
# print(type(print))

# def echo(name, age=11):
    # return "你好，我是{},今年{}岁".format(name,age)
# print(echo("liujie",21))
# print(echo("liujie"))

# list = ["nihao"]
# dict = dict(name="liujie", age=21)
# str1 = "hello world"
# flag = True

# def change(arg):
    # if str(type(arg)) == "<class 'list'>":
        # arg.append("yinshi")
    # elif str(type(arg)) == "<class 'dict'>":
        # arg.update({"xinbaji":"man"})
    # elif str(type(arg)) == "<class 'str'>":
        # arg = "hahahahaha"
    # elif str(type(arg)) == "<class 'bool'>":
        # arg = False
    
    
# change(list)
# change(dict)
# change(str1)
# change(flag)
        
# print(list)
# print(dict)
# print(str1)
# print(flag)

# def echo(*name):
    # print(type(name))
    # for i in name:
        # print(i)
        
# echo("liujie", "yinshi", "shenle")        


# def echo(**dict):
    # print(type(dict))
    # for key,value in dict.items():
        # print("{}={}".format(key, value))
# echo(name1="liujie", name2="yinshi", name3="shenle")   

# def demo(name, age=21, *address, **other):
    # print("姓名： %s" % name)
    # print("年龄： %d" % age)
    # for i in address:
        # print("家庭住址： %s" % i)
    # print("其他信息：")
    # for key,value in other.items():
        # print("%s-%s" % (key, value))
# demo("yinshi", 20, "中国", "湖南", phone="13142075842", QQ="1411068461" )

# 递归算 1-100 的加法
# def demo(num):
    # if num == 1:
        # return 1
    # return num * demo(num-1)
# print(demo(5))

# def sum(num):
    # if num == 1:
        # return demo(1)
    # return demo(num) + sum(num-1)
# print(sum(3))

# str1 = " hello world"
# print(str1.center(20)) # 就是在字符串的两边填充空格
# print(str1.find("w")) # 判断字符串中是否包含某个子字符串，和in类似，但是在包含这个子字符串的情况下，find 能返回
# print(str1.find("0"),3,5) # 这个子字符串所在的索引位置，如果不包含，那就会返回 -1,后面还可以使用参数来限制在指定的索引范围内查找
# print(str1.upper())
# print(str1.lower())
# print(str1.capitalize())#首字母大写，但是如果首字母是空格，则该函数无效


# def demo(num):
    # if num == 100:
        # return 100
    # return num + demo(num + 1)
    
# print(demo(1))


# def demo():
    # """
        # 这是demo()方法的注释
    # """
    # str1 = "nihao"
    # str2 = "woshi"
    # print(globals())
    # print(locals())
    
# demo()
# print(demo.__doc__)

# def out_function(num):
    # def in_function(num2):
        # nonlocal num 
        # num += 20
        # return num + num2
    # return in_function
# result = out_function(100)
# print(result(20))

# def add(x, y):
    # return x + y
# sum = lambda x,y:x+y
# print(add(10, 20))
# print(sum(10, 20))
    
# print(__name__)   

# str1 = "print('hello')"
# eval(str1)

# str1 = '("shenle", "yinshi")'
# str2 = '["shenle", "yinshi"]'
# str3 = '{"one":"shenle", "two":"yinshi"}'
# tuple_str1 = eval(str1)
# list_str2 = eval(str2)
# dict_str3 = eval(str3)
# print("tuple_str1: %s, 序列类型为： %s" % (tuple_str1, type(tuple_str1)))
# print("list_str2: %s, 序列类型为： %s" % (list_str2, type(list_str2)))
# print("dict_str3: %s, 序列类型为： %s" % (dict_str3, type(dict_str3)))

# temp_code="for i in range(1,5): print(i)"
# temp_compile = compile(temp_code,'','eval')
# exec(temp_compile)

# def out_function(num):
    # def in_function(num2):
        # #nonlocal num  # 必须使用 nonlocal，否则会报错
        # num = 0
        # num += 20
        # return num + num2
    # return in_function
# result = out_function(100)
# print(result(20))

# str = '''def hello():
       # print 'hello'''
# print(str)   

# str = '''def hello():
    # print('hello')
# hello()'''
# c = compile(str, '', 'exec')
# exec(c)

# import sys
# print("程序包含模块：%s" % sys.modules )
# print("程序加载路径：%s" % sys.path )
# print("程序运行平台：%s" % sys.platform )
# print("程序默认编码：%s" % sys.getdefaultencoding )

# import sys
# for item in sys.argv:
    # print(item, end=",")

# import copy
# menber_info = dict(name = "liujie", interest = ["打游戏", "看电视"])
# copy_info = menber_info
# copy_info.update(sex="man")
# copy_info["interest"].append("睡觉")
# print("menber_info: %s " % menber_info)
# print("copy_info: %s " % copy_info)

#浅拷贝
# import copy
# menber_info = dict(name = "liujie", interest = ["打游戏", "看电视"])
# copy_info = copy.copy(menber_info)
# deepcopy_info = copy.deepcopy(menber_info)
# # copy_info.update(sex="man")
# # copy_info["interest"].append("睡觉")
# print("menber_info: %s " % id(menber_info))
# print("copy_info: %s " % id(copy_info))
# print("deepcopy_info: %s " % id(deepcopy_info))
# print("+++++++++++++++++++++++++++++++++++++++++")
# copy_info.update(name="yinshi")
# copy_info["interest"].append("睡觉")
# print("menber_info: %s " % menber_info)
# print("copy_info: %s " % copy_info)
# print("deepcopy_info: %s " % deepcopy_info)


#浅拷贝
# import copy
# menber_info = dict(name = "liujie", interest = ["打游戏", "看电视"])
# copy_info = copy.copy(menber_info)
# copy_info.update(name="yinshi")
# copy_info["interest"].append("睡觉")
# print("menber_info: %s " % menber_info)
# print("copy_info: %s " % copy_info)


#深拷贝
# import copy
# menber_info = dict(name = "liujie", interest = ["打游戏", "看电视"])
# deepcopy_info = copy.deepcopy(menber_info)
# deepcopy_info.update(name="yinshi")
# deepcopy_info["interest"].append("睡觉")
# print("menber_info: %s " % menber_info)
# print("copy_info: %s " % deepcopy_info)

# #偏函数
# from functools import partial
# def add(a,b,c):
    # return a+b+c
# partial_function = partial(add, 100, 200)
# print(partial_function(30))
# print(partial_function(50))

# from random import *
# number = [item * 2 for item in range(1,11)]
# print("生成的序列： %s" % number)
# result = []
# for i in range(5):
    # result.append(choice(number))
# print("从生成的序列中随机抽取的五个数字： %s" % result)


# number = [1,2,3,4,5,6,7,8,9]
# #过滤，得到所有能被2整除的数
# filter_result = list(filter(lambda item: item % 2 == 0, number))
# print(filter_result)

# #处理，将所有的数乘二
# map_result = list(map(lambda item: item * 2, filter_result))
# print(map_result)

# #统计， 得到所有数字的和，filter 和 map 是默认提供的，但是reduce 不是，使用reduce 之前需要导入 functools模块
# from functools import reduce
# reduce_result = reduce(lambda x,y: x+y, map_result)
# print(reduce_result)

def sayHello():
    return "hello world"


















