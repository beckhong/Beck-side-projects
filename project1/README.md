# Project1: 利用flask建立第一個自己的MySQL Docker Images

## Target1: 創建Mysql docker images並透過flask來執行MySQL的CRUD

### 寫一個自己的Dockerfile

在撰寫dockerfile前的前置作業：

* 作業系統： ubuntu16.04（使用docker image）
* 安裝Python3.5.2： python3.5 python3.5-dev python3-pip
* 安裝MySQL: mysql-server
* Python需要用到的packages： requirements.txt
```
# requirements.txt
Flask==1.0.2
mysqlclient==1.4.2 # pip3 install之前需安裝libmysqlclient-dev
```
主要目錄取名為project1，架構如下(會持續更新)：
```
├── apps
│   ├── app.py
│   ├── dbconnect.py
│   └── MySQL
│       └── book_shop.sql
├── dockerfile
├── README.md
├── requirements.txt
└── run-apps.sh
```

### 安裝問題紀錄
在安裝過程中會有這個錯誤訊息：
```
debconf: delaying package configuration, since apt-utils is not installed
```
則我們在安裝apt-utils就ok了。但事情還沒完呢，出現其他錯誤訊息：

```
debconf: unable to initialize frontend: Dialog
debconf: (TERM is not set, so the dialog frontend is not usable.)
debconf: falling back to frontend: Readline
debconf: unable to initialize frontend: Readline
debconf: (This frontend requires a controlling tty.)
debconf: falling back to frontend: Teletype
dpkg-preconfigure: unable to re-open stdin: 
```
在dockerfile裡面添加

    ENV DEBIAN_FRONTEND noninteractive

加至安裝之前就不會出現了。而安裝MySQL部份，在使用docker安裝mysql-server的過程中，會出現下列狀況：
```
While not mandatory, it is highly recommended that you set a password for the
MySQL administrative "root" user.

If this field is left blank, the password will not be changed.

New password for the MySQL "root" user:
```
就算打了password，畫面就卡在這了，這時我們只要在dockerfile裡面添加就ok了。
```
{ \
    echo debconf debconf/frontend select Noninteractive; \
    echo mysql-community-server mysql-community-server/data-dir \
        select ''; \
    echo mysql-community-server mysql-community-server/root-pass \
        password ''; \
    echo mysql-community-server mysql-community-server/re-root-pass \
        password ''; \
    echo mysql-community-server mysql-community-server/remove-test-db \
        select false; \
} | debconf-set-selections \
```

最後要啟動我們的腳本run-apps.sh，其中腳本要更改權限，才不會啟動container時失敗。


### 執行dockerfile
建立docker image及建立docker container如下：
```
sudo docker build -t project1:mysql .
sudo docker run -p 8000:8086 -itd project1:mysql
```

在google chrome分別執行：
```
http://0.0.0.0:8000/
http://0.0.0.0:8000/test-connection/
http://0.0.0.0:8000/bookshop/
```

其結果應該分別為：
```
# http://0.0.0.0:8000/
Hello! My name is beck.

# http://0.0.0.0:8000/test-connection/
Connecting mysql server~

# http://0.0.0.0:8000/bookshop/
{
  "books": [
    [
      1, 
      "The Namesake", 
      "Jhumpa", 
      "Lahiri", 
      2003, 
      32, 
      291
    ], 
    [
      2, 
      "Norse Mythology", 
      "Neil", 
      "Gaiman", 
      2016, 
      43, 
      304
    ], 
     ...
     ,
    [
      16, 
      "Consider the Lobster", 
      "David", 
      "Foster Wallace", 
      2005, 
      92, 
      343
    ]
  ], 
  "content": [
    "book_id", 
    "title", 
    "author_fname", 
    "author_lname", 
    "released_year", 
    "stock_quantity", 
    "pages"
  ]
}
```

接下來要透過flask新增MySQL CRUD（C: Create, R: Read, U: Update, D: Delete)的內容。


* Reference:
    * MySQL in Docker frozen at root password config: https://stackoverflow.com/questions/38356219/mysql-in-docker-frozen-at-root-password-config
    * Getting tons of debconf messages unless TERM is set to linux- https://github.com/phusion/baseimage-docker/issues/58#issuecomment-57900765
    * 制作镜像时出现debconf: unable to initialize frontend: Dialog: https://blog.csdn.net/qq_35904833/article/details/80662683
