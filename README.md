<p align="center">
  <img alt="XueLuoPDF" src="assets/app-icon/hicolor/256x256/apps/ai.storyteller.xueluopdf.png" width="128">
</p>

<h1 align="center">雪落 PDF · XueLuoPDF</h1>

<p align="center">
  <b>基于PDFcraft制作的个人练习使用的软件</b><br>
  <b>非常感谢PDFcraft的开源</b><br>
  阅读、批注、填表、签名、整理、合并、拆分、保护，一个原生应用全搞定。<br>
  macOS · Windows · Linux · FreeBSD · 浏览器
</p>


<p align="center">
  <img alt="License: MIT OR Apache-2.0" src="https://img.shields.io/badge/license-MIT%20OR%20Apache--2.0-12a58a">
  <img alt="Written in Rust" src="https://img.shields.io/badge/written%20in-Rust-0a7563">
  <img alt="Platforms: macOS, Windows, Linux, FreeBSD, web" src="https://img.shields.io/badge/runs%20on-macOS%20%C2%B7%20Windows%20%C2%B7%20Linux%20%C2%B7%20FreeBSD%20%C2%B7%20web-12a58a">
  <img alt="No account, no telemetry" src="https://img.shields.io/badge/no%20account-no%20telemetry-0a7563">
</p>

<p align="center">
  <a href="https://github.com/PLSshenyun/xueluopdf"><b>github.com/PLSshenyun/xueluopdf</b></a> ·
  <a href="https://github.com/PLSshenyun/xueluopdf/issues">问题反馈</a> ·
  <a href="#下载">下载</a>
</p>

---

## 这是什么

XueLuoPDF 是一个本地优先的 PDF 应用：文档不离开你的电脑，没有账号、没有遥测、没有云端处理。它把 PDF 的对象结构当作数据模型，保存时默认**增量写入**——原始字节原样保留，新的改动追加在后面。

工程上它是一个 Cargo 工作区（约 30 个库 crate + 3 个可执行程序），引擎与界面分层：解析、渲染、编辑都在可复用的库 crate 里，界面只是最上面可替换的一层。同一个代码库同时产出桌面版、命令行版和 WebAssembly 浏览器版。

> 本项目基于 **PdfCraft**（[storytold/pdfcraft](https://github.com/storytold/pdfcraft)）改名而来，原作者与项目介绍见文末[「上游」](#上游)。

## 上游

XueLuoPDF 基于 **PdfCraft**（[storytold/pdfcraft](https://github.com/storytold/pdfcraft)）改名而来，原作者与项目介绍属于他们；本仓库只是换了名称与图标，引擎、界面与文档主体都是上游的工作成果。两者的授权相同（MIT OR Apache-2.0），上游的 ArtCraft 商标素材按授权要求已从本仓库移除。

Adobe、Photoshop、Illustrator、Premiere Pro、Lightroom、Acrobat、After Effects 与 InDesign 是 Adobe Inc. 在美国和其他国家的商标或注册商标。XueLuoPDF 是独立的开源项目，与 Adobe Inc. 无隶属关系，也未获得其赞助或认可；上述名称仅用于说明它所兼容的工作流。
