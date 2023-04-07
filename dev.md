# client-ci

[:point_right: 点击进入文档首页](http://baidu.com)

## 在线编写
直接修改 gitlab仓库里对应文件，提交即可，eg:
- [项目](http://baidu.com)

## 本地编写
- clone 本项目到本地
  ```sh
    git clone https://github.com/bothinli/note.git
  ```
- 修改docs文件夹内的 markdown文件后，启动本地服务器预览
	```sh
	cd docs & python -m http.server 3000
	```
- 打开 [http://localhost:3000](http://localhost:3000) 预览

### 更好的编写体验
- 安装 node.js
- 全局安装 docsify
  ```sh
  npm i docsify-cli -g
  ```
- 进入到项目根目录
  ```sh
  docsify serve docs
  ```
  修改文档后实时生效
