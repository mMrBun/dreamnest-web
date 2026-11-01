# 拖把待办 / Mop To-Do Web

拖把待办的产品介绍、技术支持和隐私网站。沿用原 `dreamnest-web` 仓库与 Vercel 静态部署方式，不需要安装依赖或设置构建命令。

## 页面

| 用途 | 路径 |
| --- | --- |
| 中文产品首页（包含帮助、联系方式及完整隐私政策） | `/` |
| English product page | `/index.en.html` |
| 中文技术支持 | `/support.html` |
| English support | `/support.en.html` |
| 简体中文隐私政策 | `/privacy-policy.zh-Hans.html` |
| English privacy policy | `/privacy-policy.html` |
| 繁體中文隐私政策 | `/privacy-policy.zh-Hant.html` |
| 日本語隐私政策 | `/privacy-policy.ja.html` |
| 한국어隐私政策 | `/privacy-policy.ko.html` |

`vercel.json` 保留 `cleanUrls: true` 与 `trailingSlash: false`，因此线上也支持不带 `.html` 的地址。原有的根路径与四个本地化隐私路径保留；根路径内仍有可展开的完整隐私政策。

## 原链接与发布

继续使用原 Vercel 项目、仓库绑定及域名，无需另建项目或改 DNS。提交并推送更新到 Vercel 关联的生产分支后，等待部署成功。

原网址为 https://dreamnest.mrbun.cn/。App Store Connect 可以这样填写：

- 营销网址：`https://dreamnest.mrbun.cn/`
- 技术支持网址：`https://dreamnest.mrbun.cn/support`（原根网址也包含支持内容，可继续使用）
- 隐私政策网址：`https://dreamnest.mrbun.cn/privacy-policy.zh-Hans`
- 英语支持与隐私：`https://dreamnest.mrbun.cn/support.en`、`https://dreamnest.mrbun.cn/privacy-policy`

以上链接需在部署成功后使用。站点没有虚构 App Store 下载链接；获得正式商品链接后，可再在首页加入下载入口。

## 本地预览与维护

```sh
python3 -m http.server 8000
```

在浏览器打开 `http://localhost:8000`。本地标准静态服务器使用带 `.html` 的页面链接；无扩展名跳转由线上 Vercel 负责。

- 首页和支持页：直接编辑 HTML。`index.md` 是产品介绍的文本版。
- 隐私政策：修改对应的 `privacy-policy*.md`，运行 `python3 scripts/build-policies.py`，会生成五种语言 HTML，并同步两种语言首页内的完整政策。脚本只使用 Python 3 标准库。
- `scripts/chrome.json` 保存生成政策页使用的页头、页脚；修改公共导航时同步更新。
- `assets/app-icon.png` 来自当前拖把待办应用图标。
- `demo.js` 仅处理示意清单的勾选与进度，不保存数据或发起请求；禁用 JavaScript 后正文、支持、政策与原生折叠交互仍可使用。
- `app-ads.txt` 保留原路径，内容已改为无广告说明，移除旧产品的广告商授权。

开发者：徐辉（Hui Xu） · 联系：mr__bun@163.com

内容依据当前应用代码：文件夹、备注、最多六张图片、日期和时间提醒、地点信息、小组件、六套配色、可选 iCloud、最近删除、备份和一次性自愿支持。未加入重复任务、番茄钟、多人协作等尚未实现的功能。
