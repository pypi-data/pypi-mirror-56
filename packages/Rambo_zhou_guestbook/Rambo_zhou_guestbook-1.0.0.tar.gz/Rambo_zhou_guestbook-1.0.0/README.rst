开发流程

更改依赖库

1 更新“setup.py”的“install.requires”
2 按以下流程更新环境：：

  (.venv)$ virtualenv --clear .venv
  (.venv)$ pip install -e ./guestbook
  (.venv)$ pip freeze > requirements.text


3 将setup.py和requirements.txt提交到版本库


$ hg clone https://rambo_zhou@bitbucket.org/rambo_zhou/guestbook
$ cd guestbook
$ virtualenv .venv
$ source .venv/bin/activate
(.venv)$ pip intall .
(.venv)$ guestbook
*Running on....
