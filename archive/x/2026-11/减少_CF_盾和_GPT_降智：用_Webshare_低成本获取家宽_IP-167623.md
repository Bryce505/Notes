# 减少 CF 盾和 GPT 降智：用 Webshare 低成本获取家宽 IP

- 原文链接：https://x.com/yuchenmax/status/2073633036915167623?a=ZuENQiZWeR428t3_35Q&s=19
- 作者：yuchen @yuchenmax
- 发布时间：2026-07-05
- 剪藏时间：2026-11-08 08:47

---

为什么需要家宽 IP

很多人用普通机场或数据中心代理访问海外服务，最烦的不是慢，而是风控。

比如 Cloudflare 验证反复弹，ChatGPT 容易降智、限制功能，部分网站还会直接拒绝数据中心 IP。

家宽 IP 的作用，就是把出口换成更像普通家庭网络的地址。它不能保证 100% 绕过风控，但通常可以减少触发 CF 盾，降低 GPT 降智和账号风控概率。

这篇文章主要讲三件事：

怎么用 #Webshare 低成本买一个静态住宅 IP

怎么检测和更换 IP

怎么接到 #Clash 里做链式代理

Webshare 购买

Webshare 是一个代理服务平台，本文主要用它的 Static Residential 静态住宅 IP：价格低、支持按带宽购买，也可以随时更换 IP。下面是购买流程。

1.注册

没有账号的先注册：Webshare

可以用邮箱注册，也可以用 Google 账号登录

已有账号直接登录即可

[图片]

[图片]

2. 购买住宅 IP

依次点击 Plans & Pricing -> Static Residential -> Add Plan

[图片]

3.类型选 Private，数量选 Custom，输入 1 后保存。Bandwidth 按自己的用量选，一般 250G 就够了

[图片]

4.地区按需选择，我这里选的是美国

[图片]

5.剩下的保持默认即可，后续都可以修改

[图片]

年付一般是 7 折。不放心可以先买一个月，后面再升级成年付

[图片]

6.点击继续

[图片]

[图片]

7.如果没有添加过支付方式，需要先添加。国内发行的 Visa、万事达卡都可以，也可以用 Google Pay。添加完成后再付款

[图片]

[图片]

8.点击 View Proxy List，跳转到代理列表

[图片]

这个页面可以看到节点的 IP、端口、账号和密码

[图片]

IP 质量检测

推荐直接用 IPQuality 这个开源项目提供的脚本检测

[图片]

HTTP 代理和 SOCKS5 代理地址，都可以在 Proxy List 页面获取

效果截图：

[图片]

也可以先用下面几个网站做初筛。结果仅供参考，最终以 IPQuality 的检测结果为准

https://www.ping0.cc/ 可以看 IP 位置和 ASN，其他信息仅供参考

https://ippure.com/ 可以看人机流量占比、IP 来源属性

https://iprisk.top/ Scamalytics 欺诈评分和 IPQuality 检测结果基本一致

IP 更换

在 Proxy List 页面点击 Replace Proxy

[图片]

ASN 推荐看这几个：

Chiller-City (20012)：小众美国家宽，可能用的人少，目前 IP 比较干净

Rcn-As (6079)：主要在美国东部，刷出 72.1.x.x 就可以用，但不是全绿

As-Wave-1 (11404)：主要在美国西部，质量不如 Rcn-As (6079)

AT&T (7018)：美国主流家宽，但一直没货。如果 ASN 列表里有，可以试一下

Comcast-7015 (7015)：美国主流家宽，名气太大，用的人很多，IP 质量一般

Charter-20115 (20115)：同 Comcast-7015 (7015)

[图片]

更换成年付

如果一开始按月购买，选好 IP 后可以切换成年付。年付一般是 7 折，当前套餐会折算成积分抵扣，不会浪费

点击 Plans & Pricing -> Edit Plan，可以按需修改配置

[图片]

我已经是年付了，所以这里显示 0

[图片]

链式代理配置

不会配置的，建议先看我之前的文章

[图片]

1.添加 proxy-providers，方便管理多个节点

节点的 IP、端口、账号和密码可以在 Proxy List 列表页面获取

[图片]

2.添加 Dialer 中转节点

自行选择使用哪个中转节点，type 也可以改成 url-test 自动选择

[图片]

3.使用节点

给需要使用该代理的代理组添加 PP-CLEAN-IP，比如 🤖 AI 服务

[图片]

文章列表

1. 小白也能轻松学会的 Clash 配置
