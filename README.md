<div align="center">
    <img src="https://raw.githubusercontent.com/leiyi2000/dst-bot/main/docs/logo.png" style="width:200px; height:200px; border-radius:50%; display:block; margin:auto;" />
</div>


![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/leiyi2000/dst-bot/main.yml)

# dst-bot
饥荒查询机器人，如果使用[wendy](https://github.com/leiyi2000/wendy)开服将支持更多指令。


### 功能

指令 | 结果 | 样例 | 描述
---- | --- | --- | ---
查服 | 编号: 1<br>存档: 小萌新注定只能吃注水肉丸啦<br>在线人数: 6 | 查服萌新 | 按房间名模糊搜索房间信息默认返回10条内容
查玩家 | 编号: 3<br>存档: 棱镜长期<br>玩家: 大明<br>在线人数: 3<br>天数: 1209<br>季节: autumn<br>直连: c_connect("113.31.186.221", 10053) | 查玩家大明 | 按玩家名模糊搜索房间默认返回10条内容
查房 | 存档: 棱镜长期<br>玩家: ['大明']<br>天数: 1218<br>季节: winter<br>直连: c_connect("113.31.186.221", 10053)<br>在线人数: 1<br>介绍: QQ群: 908262651 | 查房1 | 给定编号查询游戏房间更多信息
ls |  本群服务器如下: <br>2. 纯萌新勿入短期混档勿入禁选韦伯和沃特秒踢<br>3. [长期]纯净档-蜘蛛森林<br>7. 棱镜长期 | ls | 查询由wendy托管的游戏服 (需使用[wendy](https://github.com/leiyi2000/wendy))
备份 | <div align=""><img src="https://raw.githubusercontent.com/leiyi2000/dst-bot/main/docs/r1.png" style="width:200px; height:100px;" /></div> | 备份1 | 将会备份指定存档以QQ文件的形式发送到群内 (需使用[wendy](https://github.com/leiyi2000/wendy))
开服 | OK | 开服温蒂 或者 开服温蒂-123456 | 房间名: 温蒂 密码：123456 (需使用[wendy](https://github.com/leiyi2000/wendy) + 管理权限)
文件开服 | OK | 文件开服 Cluster_1.zip | 需先发送文件Cluster_1.zip到群内或单独聊天，后发送命令开服 (需使用[wendy](https://github.com/leiyi2000/wendy) + 管理权限)
重启 | OK | 重启1 | 重启由wendy托管的游戏服 (需使用[wendy](https://github.com/leiyi2000/wendy) + 管理权限)
回档 | OK | 回档1-3 | 将回滚3天存档编号为1的存档 (需使用[wendy](https://github.com/leiyi2000/wendy) + 管理权限)
关服 | OK | 关服1 | 关闭由wendy托管的游戏服 (需使用[wendy](https://github.com/leiyi2000/wendy) + 管理权限)
重置 | OK | 重置1 | 重置由wendy托管的游戏服 (需使用[wendy](https://github.com/leiyi2000/wendy) + 管理权限)

## 快速部署
- 拉取项目
  ```shell
  git clone https://github.com/leiyi2000/dst-bot.git
  ```

- 环境变量

  [修改.env.example为.env](.env.example)

- 运行
  ```shell
  cd dst-bot && source .env && docker compose up -d
  ```

- 添加管理权限
  ```shell
  curl -X 'POST' \
    'http://127.0.0.1:8000/admin' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "uid": "QQ"
  }'
  ```

- [接口文档](http://127.0.0.1:8000/docs)

  http://127.0.0.1:8000/docs


## 感谢
- 感谢NapCatQQ项目地址：https://github.com/NapNeko/NapCatQQ
