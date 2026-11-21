# CC Desk Tunnel：把 Claude Code 搬到 VPS

- 原文链接：https://x.com/jackluos3lpo/status/2123769954747256839?a=N3PjsdMYfWxvCSMGVn8&s=19
- 作者：jackluos @jackluos3lpo
- 发布时间：2026-11-20
- 剪藏时间：2026-11-21 14:28

---

Claude Code 装本机怕封号？有人把 Claude 搬到 VPS 上了，本机照样直接开发

新焚决来了
CC Desk Tunnel，开源的，GitHub 578 星

思路很简单
Claude Code 不装你电脑上
装到国外 VPS 的 Docker 里跑，跑的还是官方原版，没改本体
你本机只装一个桌面客户端连过去

神奇的是体验
项目文件、编译器、编辑器全在本机
Claude 通过一条加密反向隧道，直接读写你本机项目、跑你本机的命令
用起来跟本地装的一模一样
不用远程桌面来回倒腾代码了

为啥这么折腾
模型请求全从服务器出去
本机不留运行环境
主打一个降低封号风险
作者自己开新号这么用了一周，号还活着

配置要求还低
活都在本机干，服务器只跑 Claude Code
2 核 1G 的小鸡就够
Windows 不用开任何入站端口
Win、Linux、macOS 客户端都有，还带个终端版 ccdt

项目地址
https://github.com/sun168567/cc-desk-tunnel
