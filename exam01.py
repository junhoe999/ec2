# client -> server (Request)
# server -> client (Response)

# python server의 종류
# 1) flask  : 마이크로 웹 프레임워크
# 2) Django : 풀스택 웹 프레임워크(flask보다 대략 10 ~ 20 무겁다)

from flask import Flask             # route 경로, run 서버를 실행하는 class
from flask import render_template   # html load ft.
from flask import request           # 사용자가 보낸 정보와 관련된 ft.
from flask import redirect          # 페이지 이동 ft.
from flask import make_response     # 페이지 이동 시, 정보 유지하기 위한 ft.    

from aws import detect_labels_local_file  # AWS Rekognition을 사용하기 위한 ft.
from aws import compare_faces as cf # 얼굴 비교를 위한 ft.


# 파일이름 보안처리 library
from werkzeug.utils import secure_filename

import os
#static folder가 없다면 만드는 동작 구현
if not os.path.exists("static"):
    os.makedirs("static")


app = Flask(__name__)
@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/compare", methods=["POST"])
def compare_faces():
    
    # 1. compare로 오는 file 1, 2를 받아서
    # static 폴더에 save
    # 이 때, secure_filename을 사용하여 파일 이름을 안전하게 처리
    if request.method == "POST":
        file1 = request.files["file1"]
        file2 = request.files["file2"]

        file1_filename = secure_filename(file1.filename)
        file2_filename = secure_filename(file2.filename)
        
        file1.save(f"static/{file1_filename}")
        file2.save(f"static/{file2_filename}")

        result = cf(f"static/{file1_filename}", f"static/{file2_filename}")
        
    return result


@app.route("/detect", methods=["POST"])
def detect_label():
    # flask에서 보안 규칙상
    # file이름을 secure처리 해주어야 함
    if request.method == "POST":
        file = request.files["file"]

        filename = secure_filename(file.filename)  # 파일이름 보안처리
        # file을 static folder에 저장하고
        file.save(f"static/{filename}")
        # 해당 경로를 detect_local_~ ft에 전달
        r = detect_labels_local_file(f"static/{filename}")
        
        
        
        return r


@app.route("/secret", methods=["POST"])
def box():
    try:
        if request.method == "POST":
            # 사용자가 보낸 정보
            # request.form["key"]
            hidden = request.form["hidden"]
            return f"비밀정보 : {hidden}입니다."
    except:
        return "오류 발생 "

@app.route("/login", methods=["GET"])
def login():
    if request.method == "GET":
        # 페이지가 이동하더라도
        # 정보를 남겨 사용
        login_id = request.args["login_id"]
        login_pw = request.args["login_pw"]
        if login_id == "junhoe99" and login_pw == "1234":
            response = make_response(redirect("/login/success"))
            response.set_cookie("user", login_id)
            return response
        else:
            return redirect("/")

    return "로그인 성공"

@app.route("/login/success", methods=["GET"])
def login_success():
    if request.method == "GET":
        # 페이지가 이동하더라도
        # 정보를 남겨 사용
        login_id = request.cookies.get("user")
        return f"{login_id}님, 환영합니다."




if __name__ == "__main__":
    app.run(host="0.0.0.0")