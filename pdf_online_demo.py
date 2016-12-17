import os
import time
import json
from flask import jsonify
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

UPLOAD_FOLDER = './static/doc'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # 设置文件上传的目标文件夹


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/upload', methods=["GET", "POST"])
def upload_test():
    return render_template("upload.html")


@app.route('/show', methods=["GET", "POST"])
def show_test():
    return render_template("show.html")


@app.route("/api/upload", methods=["GET", "POST"])
def upload():
    file = request.files.get("file_data")
    msg = api_upload(app, file)
    upload_msg = json.loads(msg.data.decode("utf-8"))
    errmsg = upload_msg.get("errmsg")
    return jsonify({"msg": errmsg})


def api_upload(app_boj, file):
    basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前项目的绝对路径
    file_dir = os.path.join(basedir, app_boj.config['UPLOAD_FOLDER'])  # 拼接成合法文件夹地址
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # 文件夹不存在就创建
    fname = file.filename
    ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
    unix_time = int(time.time())
    new_filename = str(unix_time)+'.'+ext   # 修改文件名
    file.save(os.path.join(file_dir, new_filename))  #保存文件到upload目录
    return jsonify({"result": 1, "new_name": new_filename, "errmsg": "上传成功"})


if __name__ == '__main__':
    app.run(debug=True)
