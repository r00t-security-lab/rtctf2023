from flask import Flask, render_template, request, make_response, redirect

app = Flask(__name__)

# 设置 flag
FLAG = 'CTF{7HE_R00T_15_Fun}'

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/')
def modify_header():
    if 'X-Forwarded-For' in request.headers:
        new_xff = request.headers['X-Forwarded-For']
        if new_xff == '127.0.0.1':
            response= make_response(redirect('/modify_referer'))
            return response
        if new_xff != '127.0.0.1':
                return render_template('error.html')
    return render_template('modify_header.html')

@app.route('/modify_referer')
def modify_referer():
    if 'Referer' in request.headers:
        new_referer = request.headers['Referer']
        if new_referer == 'CTF.com':
            return render_template('flag.html') 
        if new_referer != 'CTF.com':
            return render_template('error.html')
    return render_template('modify_referer.html')

@app.route('/flag')
def get_flag():
    if 'X-Forwarded-For' in request.headers and 'Referer' in request.header:
        if request.headers['X-Forwarded-For'] == '127.0.0.1'and request.headers['Referer'] == 'CTF.com':
            return render_template('flag.html') 
    return render_template('error.html') 
        
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8082, debug=False)
