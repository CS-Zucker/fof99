import re
from flask import Flask, make_response, render_template, jsonify, request
from crawl import crawls, rank, get_per
from inv_normal import invest
from inv_days import different_day_income
from get_radar import get_radars
import pandas as pd

import fund_list

# 创建一个app
app = Flask(__name__)


# 准备一个函数来处理浏览器发来的请求
@app.route('/')
def show():
    return render_template('show.html')

# 准备一个函数来处理浏览器发来的请求
@app.route('/show_info')
def show_info():
    return render_template('show_info.html')


# 服务器准备好接受静态页面，下同
@app.route('/beijin')
def beijin():
    return render_template('beijin.html')


@app.route('/guangdong')
def guangdong():
    return render_template('guangdong.html')


@app.route('/shanghai')
def shanghai():
    return render_template('shanghai.html')


@app.route('/qita')
def qita():
    return render_template('qita.html')


# 获取前端'搜索'传入的基金编号，传入300个交易日的内容
@app.route('/api', methods=['GET', 'POST'])
def get_data():
    if request.method == 'GET':
        key = request.args.get('key')
        value = crawls(key, '300')
        return jsonify({'value': value, 'success': 0})

# 获取前端'表单'传入的基金编号，传入300个交易日的内容
@app.route('/jz_api', methods=['GET', 'POST'])
def get_jz():
    if request.method == 'GET': 
        fund_key_str = request.args.get('key')  
        fund_keys = re.findall(r'\b\d{6}\b', fund_key_str)
        print(type(fund_keys))
        jz_value = crawls(fund_keys[0], '300')
        print(jz_value['title'])
        return jsonify({'value': jz_value, 'success': 0})



# 获取show_info传入的基金 编号|名称，传入基金搜索的结果
@app.route('/info_api')
def get_info():
    fundkey = request.args.get('key')
    value = fund_list.fund_list_select_db(fund_key=fundkey)
    return jsonify({'value': value, 'success': 0})

# 返回基金公司的信息给前端js，让前端渲染画面
@app.route('/company')
def get_weather():
    data = pd.read_csv('./static/company.csv')
    dic = data[['name', 'scale', 'count', 'url']]
    dic = dic.to_dict(orient='list')
    return dic


# 获取前端传回来的想要获取的基金类型的排行，并把内容返回给js
@app.route('/rank')
def get_rank():
    id = request.args.get('id')
    datas = rank(id)
    return jsonify({'value': datas, 'success': 0})


# 获取前端传入的基金编号，将基金的投资信息返回给js
@app.route('/inst')
def get_inst():
    keys = request.args.get('values')
    value = get_per(keys)
    return jsonify({'value': value, 'success': 0})


# 将预测结果返回给js，下同
@app.route('/inv')
def get_inv():
    key = request.args.get('key')
    value = crawls(key, '300')
    money = request.args.get('money')
    value = invest(value, money)
    return jsonify({'value': value, 'success': 0})


@app.route('/day')
def get_day_inv():
    key = request.args.get('key')
    value = crawls(key, '300')
    money = request.args.get('money')
    value = different_day_income(value, money)
    return jsonify({'value': value, 'success': 0})


# 绘制雷达图，返回数据
@app.route('/radar')
def get_radar():
    key = request.args.get('key')
    value = get_radars(key)
    return jsonify({'value': value, 'success': 0})


if __name__ == '__main__':
    # 运行app
    app.run()
