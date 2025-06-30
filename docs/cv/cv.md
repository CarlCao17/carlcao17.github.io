# 曹正盛
**服务端工程师** | zhsh.cao@gmail.com | 18720934114 


## 专业技能  
- **编程语言**: 熟悉 Golang 语言, 了解 Go 并发，Go runtime，内存分配，反射，AST 等
- **框架与工具**: Kitex, Hertz, GORM, 
- **数据库**: MySQL, Redis，了解 Redis 分布式锁和限流器实现
- **中间件**: RESTful API 设计, 微服务架构, 消息队列 (Kafka, Eventbus) 
- **软技能**: 团队协作, 业务导向，线上故障排查，性能瓶颈分析，代码重构与优化


## 🎓 教育背景
<div style="display: flex; justify-content: space-between; align-items: center;">
  <span style="flex:1; text-align:left;">哈尔滨工业大学（深圳）｜硕士</span>
  <span style="flex:1; text-align:center;">计算机技术</span>
  <span style="flex:1; text-align:right;">[2019.09] - [2022.01]</span>
</div>
<div style="display: flex; justify-content: space-between; align-items: center;">
  <span style="flex:1; text-align:left;">南昌大学｜本科</span>
  <span style="flex:1; text-align:center;">计算机应用科学</span>
  <span style="flex:1; text-align:right;">[2014.09] - [2018.06]</span>
</div>   

****   


## 工作经历  
<h4 style="display: flex; justify-content: space-between;">
  <span>字节跳动 | 服务端工程师  </span>
  <span>2022.02 - 至今</span>
</h4>

#### [全球商业化-广告业务-广告落地页] 
**背景**：负责 Tiktok 自建落地页服务端，B 端创编和 C 端投放，服务全球 xx+ QPS，2024 年广告消耗 $19B，效果广告渗透率 16%+。

**技术栈**：**微服务架构**，**MySQL**, **Redis**, **MQ**

1. 架构设计：B 端单元化，C 端全球多活，数据全球同步，（编译链路）容灾架构，较好地支持了落地页业务发展，整体架构在 Project U(US 禁令)中得到检验
2. C 端：利用两级缓存，支持 10W+ QPS，责任链模式支持各业务自定义逻辑；
  性能优化 & 稳定性治理：结合 PProf 火焰图，通过对 ab 参数预解析+裁剪+缓存等手段，减少了 40%+ CPU 使用率，接口 P90 时延降低了 50%+（120 ms -> 40 ms）

  通过限流器和分布式锁，
  
  建设完善落地页维度 ab 实验机制，支持 C 端实验 40+
3. B 端：建设权限中间件，AccessToken 机制，架构重构，解决历史债务问题


#### [全球商业化-广告业务-User Journey] 
业务上的各种尝试：四宫格，单品多图/单品单图， label，各种样式的尝试替换，卖点数据替换，提早展出/延迟展出，实验分析，结果回收
Web Ads 卖点 + Shop Ads 卖点
Carousel 图片治理


---

## 🏆 个人成就  
- 在 [项目名称] 中，通过优化代码和架构，将系统性能提升 50%  
- 开源项目 [项目名称] 获得 500+ GitHub Stars  
- 在公司内部技术分享会上，被评为“最佳分享者”  

---

## 💡 其他信息  
- **博客**: [你的博客链接]  
- **GitHub**: [你的 GitHub 链接]  
- **语言**: 英语 (熟练), [其他语言]  
- **兴趣爱好**: 开源贡献, 技术写作, 跑步   