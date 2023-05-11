from flask import Flask, render_template, request, make_response, redirect

app = Flask(__name__)

# 设置 flag
FLAG = 'CTF{7HE_R00T_15_Fun}'

@app.route('/', methods=['GET', 'POST'])
def index():
    # FIXME 判断条件应该为xff是否为127打头
    if request.method == 'POST':
        return redirect('/modify_header')
    return render_template('index.html')

@app.route('/index', methods=['GET', 'POST'])
def index1():
    return 'nothing', 400

@app.route('/modify_header', methods=['GET', 'POST'])
def modify_header():
    # FIXME 判断条件有问题, 应该判断referer头, 当referer头对了以后才redirect
    if request.method == 'POST':
        # 获取用户修改后的 X-Forwarded-For
        new_xff = request.headers['X-Forwarded-For']
        if new_xff is None:
            return 'Missing X-Forwarded-For header', 400
        if new_xff == '127.0.0.1':
            response= make_response(redirect('/modify_referer'))
            return response
    # FIXME xff头是用户发送的header, 而不是服务器返回的header
    return render_template('modify_header.html', header='X-Forwarded-For')

@app.route('/modify_referer', methods=['GET', 'POST'])
def modify_referer():
    if request.method == 'POST':
        # 获取用户修改后的 referer
        new_referer = request.headers['Referer']
        if new_referer is None:
            return 'Missing Referer header', 400
        if new_referer == 'CTF.com':
            response = make_response(redirect('/flag'))
            return response
    return render_template('flag.html', header='Referer')

@app.route('/flag')
def get_flag():
    return render_template('error.html', message='Access Denied')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
