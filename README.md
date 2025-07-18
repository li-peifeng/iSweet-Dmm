<p align="center">
  <a href="https://peifeng.li"><img width="184px" alt="logo" src="https://raw.githubusercontent.com/li-peifeng/li-peifeng.github.io/refs/heads/main/logo.png" />
  </a>
</p>

## 此脚本和MacOS app可以自动下载 DMM 的 JAV 高清封面
### 主要功能
- 自动模式（从文件夹获取名称）
- 手动模式（手动输入番号代码）
- 竖版海报图 (Poster)
- 横版缩略图（Thumb）
- 横版缩略图+背景图 (Thumb+Fanart)
- 全部3种封面图 (Thumb+Poster+Fanart)
- 可自动检测番号的格式并改正，比如ABC-987,ABC987,abc987等等。
- 统计成功/部分成功/失败/全部计数
- MacOS 单文件可执行app，可直接运行。

### 自动模式
可选择文件夹自动根据文件夹名称进行下载。
注意不是根据文件名哦，是最后一级的文件夹，比如 123/456/789.mkv，是提取456的名称。
### 手动模式
手动输入番号进行下载，格式会自动纠正。
此模式会下载图片至当前文件夹的 Thumb-Poster-Fanart 目录下。
### 下载全部封面图 (Thumb+Poster+Fanart)
此模式下如果有某些图片下载失败的情况下，可以保存下载成功的图片。
比如Thumb和fanart下载成功，但是poster失败，则会提示部份失败。

### 封面分辨率说明
只下载2K高清封面，有300KB阀值，小于此数值则提示失败。
