> 欢迎您参与项目的开发，下面是参与代码贡献的指南，以供参考！ヾ(ﾟ∀ﾟゞ)

# 代码贡献步骤

## 0. 提交 issue
**任何**新功能或者功能改进建议和 BUG 修复都先提交 [issue][issues] 讨论一下，再进行开发

## 1. Fork 此仓库

## 2. Clone 仓库到本地
```shell
git clone https://github.com/{YOUR_USERNAME}/Genshin-Impact-Tools.git

# 推荐使用pipenv在虚拟环境进行开发
pip install pipenv

# 安装开发环境依赖包
pipenv install -d 

# 进入虚拟环境shell
pipenv shell

# 退出虚拟环境
deactivate
```

如果你不熟悉 pipenv 虚拟环境的使用，请参照 [pipenv wiki][pipenv]

## 3. 创建新的开发分支

```shell
# 创建新分支
git checkout -b {BRANCH_NAME}
```

## 4. 编写代码和测试用例后进行代码测试

按照下列命令依次格式化你的代码，并根据 flake8 的修改意见进行修改，在无任何问题后可进行 PR

```shell
black --line-length=100 src tests

isort src tests

flake8 src tests

pytest tests

pyinstaller --clean ./main.spec
```

## 5. 提交 pull request

```shell
# 将代码推送到自己 fork 仓库的分支
git push origin {BRANCH_NAME}
```

回到自己的 GitHub 仓库页面，选择 New pull request 按钮，创建 Pull request 到原仓库的 main 分支。

然后等待 Review 即可，如有 Change Request，再本地修改之后再次提交即可。

## 6. 更新主仓库代码到自己的仓库

```shell
git remote add upstream https://github.com/cntvc/Genshin-Impact-Tools.git

git pull upstream main

git push
```

# 代码风格、格式规范

代码风格遵循 [Google python style guide](https://google.github.io/styleguide/pyguide.html)（[中文版](https://google-styleguide.readthedocs.io/zh_CN/latest/google-python-styleguide/contents.html)）

代码格式请遵循 [PEP8]，可以用自动格式化工具，如 `black`

请务必严格遵循该规范，特别是命名、空格的正确使用。在提交前，会自动运行代码检查工具，检查代码中存在的格式问题。

# 提交规范

## 提交描述

本项目采用 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/v1.0.0/) 规范，请严格遵守。

## 提交内容

确保提交的粒度足够小，比如如果同时修复了一个 bug 和增加了一个新功能，应该拆开为两次提交和 PR 。

如果你有破坏性修改（修改方法名、增加方法必需参数等），请在提交信息中的尾注部分写上 `BREAKING CHANGE: 说明`。例如：

```
fix: 给 method() 增加了一个必需参数

可选的其他描述...

BREAKING CHANGE: 给 method() 增加了一个必需参数
```

或者是在第一行冒号前加一个英文感叹号也行：

```
fix!: 给 method() 增加了一个必需参数

可选的其他描述...
```

非必要尽量不要有破坏性修改，比如如果只是新增一个参数，可以考虑一下这个参数是不是能设置个默认值。

[issues]: https://github.com/cntvc/Genshin-Impact-Tools/issues
[pipenv]: https://pipenv.pypa.io/en/latest/
