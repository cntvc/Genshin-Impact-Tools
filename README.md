# 原神小工具


## 主要功能点：
- 抽卡记录导出（由于官方限制，只能导出最近6个月抽卡记录）    
  - 可选的多种导出方式：游戏缓存（推荐）、剪切板、配置文件
- 历史记录合并
  - 支持多个数据文件同时合并，并在对应用户目录下生成抽卡报告
  - 支持的文件格式有: **`xlsx, json`**
    <details>
      <summary> 对于 <b>1.3 版本前</b> 导出的记录 </b></summary>
      <p>
    >    
    >   部分抽空数据在1.3版本前导出时无 `id` 字段，官方在1.3版本后才将其加入    
    >   由于本软件排序需要使用该字段，因此最多只能有 **1份** 文件内的抽卡数据包含无效的 id 字段，否则会导致统计结果错误    
    > 
    >   例如： 现有三份文件 `A.json`, `B.xlsx`, `C.json` 均为 `UIGF` 格式    
    >   假设 `A.json` 是由其他软件导出的，其部分原始数据无 id 项，但是导出时其他软件为缺失 id 的抽卡记录填充了 id 序列    
    >   `B.xlsx` 同样有部分数据无 id ，那么将2者合并时就无法判断抽卡顺序，导致统计错误
      </p>
    </details>
- 支持多账户使用
- 支持 [UIGF][uigf] 格式导入和导出
  > **UIGF**    
  > 统一可交换祈愿记录标准格式，可用于在不同软件间迁移数据   

软件支持的系统版本：win7，win10， win11


> <details>
>   <summary>点击查看<b>抽卡报告展示</b></summary>
>   <p>
> 
>   ![report][report]
>   </p>
> </details>


## 下载

在 [下载页面][download] 找到对应系统的软件版本下载ZIP压缩包


## 详细软件说明见 [Wiki][wiki]


## 如何反馈软件问题

- 反馈软件BUG
  > 在 [Issues页面][issues] 选择对应的反馈类型，并填写系统版本、运行日志等相关信息。
  > 
  > 将下面的路径复制到文件资源管理器地址栏即可访问日志文件
  > ```text
  > %USERPROFILE%\AppData\Local\Genshin-Impact-Tools\log
  > ```

- 其他问题请到[讨论区][discussions]进行讨论。


---
本项目根据 **[genshin-gacha-export](https://github.com/sunfkny/genshin-gacha-export)** 修改而来

[wiki]: https://github.com/cntvc/Genshin-Impact-Tools/wiki
[download]: https://github.com/cntvc/Genshin-Impact-Tools/releases/latest
[issues]: https://github.com/cntvc/Genshin-Impact-Tools/issues/new/choose
[report]: https://github.com/cntvc/Genshin-Impact-Tools/wiki/image/statistics.png
[uigf]: https://uigf.org/
[discussions]: https://github.com/cntvc/Genshin-Impact-Tools/discussions