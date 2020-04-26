import json
from flask import Flask,render_template, redirect, request, Markup, escape, flash
import datetime
import os

app = Flask(__name__)

DATA_FILE = "datafile.json"

def save_data(start, finish, memo, create_at):
    """
    saved data 
    start : 食品名
    finish : 消費期限
    memo : メモ
    create_at : 作成日
    """
    try:
        database = json.load(open(DATA_FILE, mode="r", encoding="utf-8"))
    except FileNotFoundError:
        database = []

    # create_at_date = create_at.strftime("%Y-%m-%d")

    database.insert(0, {
        "start" : start,
        "finish" : finish,
        "memo" : memo,
        "create_at" : create_at.strftime("%Y-%m-%d")
    })

    json.dump(database, open(DATA_FILE, mode="w", encoding="utf-8"), indent=4, ensure_ascii=False)

    # print("write data")

def load_data():
    try:
        database = json.load(open(DATA_FILE, mode="r", encoding="utf-8"))
    except FileNotFoundError: 
        database = []
        print("File not Found, Create new file")
    
    return database

def delete_all_logs():
    try:
        os.remove(DATA_FILE)
        
    except FileNotFoundError :
        file_status = "no_file"
    

# 項目表示用
title = "消費期限管理表"
name1 = "食品名"
name2 = "消費期限"
memo = "メモ"

@app.route("/")
def index():
    ld = load_data()
    return render_template("index.html", title=title, first=name1,\
         finish=name2, memo=memo, rides=ld)

@app.route("/save", methods=["POST"])
def save():
    start = request.form.get("start")
    finish = request.form.get("finish")
    memo = request.form.get("memo")
    create_at = datetime.datetime.now()
    save_data(start, finish, memo, create_at)

    return redirect("/")

@app.template_filter("nl2br")
def nl2br_filter(s):
    return escape(s).replace("\n", Markup("<br>"))

@app.route("/delete", methods=["POST", "GET"])
def delete():
    delete_all_logs()
    return redirect("/")

if __name__ == "__main__":
    app.run("0.0.0.0", 8080, debug=True)
