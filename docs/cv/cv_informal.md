# CV

---

## 教育背景

## 技术栈
- 熟悉 Go 语言，熟悉 Go 并发相关，了解 runtime goroutine 调度，内存分配
  - Go 哲学和设计理念
  - Go 基础：slice, map 原理，io 包，net 包, interface, 范型, error 处理
  - Go 内存序，并发原语，channel 原理，
    - 并发包 sync/mutex 实现原理，还有哪些常用的，原理
  - goroutine 如何创建，如何调度，如何抢占，栈扩张和收缩，如何复用，
    - 是否需要协程池
  - Go 内存分配
  - Go GC 
- 了解 Linux 网络编程技术栈，
  - TCP/IP 协议栈，Linux 网络栈的大致流程
  - Epoll 原理，io_uring 原理，Go 如何实现，RPC 框架 kitex 如何设计/实现
- 了解 Redis 
  - Redis 几种数据结构和实现原理，
  - 主从复制，集群模式
  - Redis 经典应用：
    - 分布式缓存（最终一致），常见问题如何解决
      - 字节缓存和对象缓存，二级缓存
    - 分布式锁，分布式锁的问题，如何解决
    - 限流器
    - 排行榜（没用过）
  - Bytedance 的 Alchemy 设计，Proxy 层设计
  - Bytedance Abase 原理
- 了解 MySQL
  - MySQL InnoDB 存储引擎了解
  - 索引，索引优化
  - 写后读
  - 分片库/分片表
  - SQL 相关
- 了解 MQ
  - 消息队列的基本原理，如何选型
  - 消息队列的一些问题，如何解决
    - 消息重复消费
    - 消息丢失
    - 消息顺序问题
  - kafka 原理，Eventbus 设计原理

## 项目

### 非中国区商业化落地页
Bytedance 2022.02 - 2025.01
B 端落地页数据管理，C 端物料准备，域名资产管理，离线数据，架构可用性和容灾，ProjectU，
背景：非中商业化广告业务，Tiktok 自建落地页站点 (Tiktok Instant Page, TIP) 项目，负责服务端方向，TIP 在效果广告大盘渗透率 16%，2024 全年广告消耗 $19B。带过两个同学
主要工作：
1. 涉及架构，容灾建设，作为落地页团队 PoC 参与商业化方向容灾建设工作
   - 参与落地页全球多活方案建设，C 端实现全球多活&单元化，B 端实现单元化
   - 
2. C 端，建设落地页维度 ab 实验机制，服务 40+ 项目 C 端实验，支持动态配置，C 端实验框架，使用 pprof 工具完成性能优化排查，降低接口时延 P99 80%+（120ms -> 30ms），CPU 峰值使用率下降 30%+（50% -> 20%），节省 40%+ CPU Core
3. 内存泄露问题
4. 通过懒刷新机制，限流和锁机制
5. 通过责任链模式和 C 端缓存机制，保障了落地页业务的 2022-2023 的快速发展
6. 利用整洁架构完成 B 端项目重构，统一鉴权体系，建设 AccessToken 机制
7. 2023-2024 期间也尝试过 Instant Page 智能生成探索项目


非中国区商业化落地页业务高速发展，主要解决从广告主创编，C 端广告投放链路，

一方面业务不断发展，广告从美国，欧洲，日本，东南亚，中东，为了应对全球用户，C 端服务全球部署，B 端业务多活单元化，编译问题如何解决。
服务架构，业务架构随着业务的发展不停演进，满足业务需要；
- 架构 & 稳定性：如何设计一个，B 端，C 端，编译链路，多活容灾；业务在不断的发展，机房建设，故障处理，下游，广告链路 200ms 限制，稳定性要求
  - 一个典型场景：US Ban 项目，B 端服务在 RoW，C 端服务无状态，数据全球各存一份，编译链路也可以完全断开，最复杂的是端上域名（落地页/图片/视频）
- 建设落地页维度 ab 实验机制

广告链路的时延和 QPS 要求：重 IO 逻辑，通过两层 Cache，C 端 model，控制下游调用（），持续性能优化和检测，DB Schema 反范式化减少 SQL 查询
  - 索引（最左匹配，根据热点查询&慢 SQL），反范式化，business_type/is_one2n
  - 针对不同 model，使用 Redis 缓存热点数据，将接口响应时间降低 40% ； 

 随着 TIP 业务拓展，我们从广告流量到自然流量，站外流量，达人带货等场景。B 端服务重构：Clean 架构
 - B 端场景：


性能优化：page_pool 优化&稳定性治理, H5 server 长尾请求优化


架构设计（解决什么问题）
B 端重构，C 端优化，，1p 和 3p 融合；C 端实验功能设计， 性能优化、稳定性
熟悉容灾和多活，全球部署，参与过 ProjectU 项目
了解 Golang 源码和设计
熟悉 Redis
熟悉 Linux 网络编程


要解决的问题？如何解决？解决收益如何？后续如何保障

项目特点
 1. 高并发 C 端，
 2. 熟悉 Go 语言项目优化


### TT 广告样式业务
Bytedance 2025.02 - 至今
业务迭代
 1. Carousel 广告图片优化项目
 2. 闭环&开环卖点项目






