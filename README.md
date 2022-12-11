# 原神小工具


## 主要功能点：
- [X] 抽卡记录导出（由于官方限制，只能导出最近6个月抽卡记录）    
  - 可选的多种导出方式：游戏缓存（推荐）、剪切板、配置文件
- [X] 历史记录合并
  - 目前只支持json格式
  - 不支持 1.3 版本前导出的记录
- [X] 支持多账户使用

软件支持的系统版本：win7，win10， win11

> <details>
>   <summary>待开发功能</summary>
>   <p>
> 
> - [ ] 本地用户系统（方便处理一些代码逻辑）
> - [ ] 国际服、云原神支持
> - [ ] XLSX 格式的历史记录合并
> - [ ] 生成抽卡统计报告（独立功能）
> - [ ] 米游社签到
> - [ ] 适配 UIGF 格式
>   </p>
> </details>

---

> <details>
>   <summary>点击查看<b>软件展示</b></summary>
>   <p>
> 
> ```shell
>                   主菜单
> ========================================
> 1.导出抽卡数据
> 2.合并抽卡记录
> 3.软件设置
> 
> 0.退出程序
> ========================================
> 请输入数字选择菜单项:
> ```
>   </p>
> </details>

# 下载

在软件最新版 [下载页面][2] 找到对应系统的软件版本下载ZIP压缩包解压
- Win10 及以上版本无后缀， 对应文件名为 `Genshin_Impact_Tools_{version}.zip`
- Win7 版本后缀为_win7， 对应文件名为 `Genshin_Impact_Tools_win7_{version}.zip`

## 详细软件说明见 [Wiki][1]

## 如何反馈软件问题

在 [Issue页面][issue] 选择对应的反馈类型，并填写系统版本、运行日志等相关信息。

将下面的路径复制到文件资源管理器地址栏即可访问日志文件
```text
%USERPROFILE%\AppData\Local\Genshin-Impact-Tools\log
```
粘贴最新日志信息或者直接粘贴日志文件到网页对应位置

---
本项目根据 **[genshin-gacha-export](https://github.com/sunfkny/genshin-gacha-export)** 修改而来

[1]: https://github.com/cntvc/Genshin-Impact-Tools/wiki
[2]: https://github.com/cntvc/Genshin-Impact-Tools/releases/latest
[issue]: https://github.com/cntvc/Genshin-Impact-Tools/issues/new/choose