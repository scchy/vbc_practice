# NextCode 发布到 VSCode 扩展商店指南

将插件发布到 Visual Studio Code Marketplace，让用户可以在 VSCode 中搜索并安装。

## 📋 发布前准备

### 1. 注册必要账户

#### 步骤 1: 注册 Azure DevOps 账户
1. 访问 https://azure.microsoft.com/services/devops/
2. 点击 "Start free" 或 "Sign in"
3. 使用 Microsoft 账户登录（或创建新账户）
4. 创建组织（Organization），例如：`nextcode-publisher`

#### 步骤 2: 创建 Personal Access Token (PAT)
1. 登录 Azure DevOps: https://dev.azure.com/{你的组织名}
2. 点击右上角用户头像 → "Personal access tokens"
3. 点击 "New Token"
4. 填写信息：
   - **Name**: `nextcode-publish`
   - **Organization**: 选择你的组织
   - **Expiration**: 选择过期时间（建议 1 年）
   - **Scopes**: 
     - 点击 "Show all scopes"
     - 找到 "Marketplace" → 勾选 "Manage"
5. 点击 "Create"
6. **立即复制 token**（只显示一次！）
   - 格式：`xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

#### 步骤 3: 创建发布者
1. 访问 https://marketplace.visualstudio.com/manage
2. 登录 Microsoft 账户
3. 点击 "Create publisher"
4. 填写信息：
   - **Publisher ID**: `nextcode`（唯一标识，小写，无空格）
   - **Publisher Name**: `NextCode`
   - **Description**: `AI-powered code completion with Chinese LLM support`
   - **Email**: 你的邮箱
   - **Website**（可选）: GitHub 仓库链接
5. 点击 "Create"

---

## 🎨 准备发布材料

### 必需文件

#### 1. 图标 (icon.png)
创建 256x256 像素的图标，放在项目根目录：
```
nextCode/
├── icon.png          # 256x256px
├── package.json
└── ...
```

图标要求：
- 尺寸：256x256 像素
- 格式：PNG
- 背景：透明或纯色
- 风格：简洁，在深色/浅色主题都可见

#### 2. 截图 (screenshots)
在 package.json 中添加截图：
```json
{
  "galleryBanner": {
    "color": "#1e1e1e",
    "theme": "dark"
  },
  "icon": "icon.png",
  "screenshots": [
    {
      "path": "screenshots/demo1.png",
      "title": "Code Completion",
      "description": "AI-powered inline code completion"
    },
    {
      "path": "screenshots/settings.png", 
      "title": "Settings",
      "description": "Easy configuration with multiple LLM providers"
    }
  ]
}
```

创建目录并添加截图：
```bash
mkdir -p nextCode/screenshots
# 添加 2-5 张截图，建议尺寸：1200x800
```

#### 3. 更新 package.json

完整配置示例：
```json
{
  "name": "nextcode",
  "displayName": "NextCode - AI Code Completion",
  "description": "AI-powered code completion with support for Chinese LLM APIs (DeepSeek, Qwen, Kimi, etc.)",
  "version": "1.0.0",
  "publisher": "nextcode",
  "engines": {
    "vscode": "^1.85.0"
  },
  "categories": ["Machine Learning", "Snippets", "Other"],
  "keywords": [
    "copilot",
    "ai",
    "code completion",
    "deepseek",
    "qwen",
    "kimi",
    "智谱",
    "通义千问",
    "国产大模型",
    "intellisense"
  ],
  "icon": "icon.png",
  "galleryBanner": {
    "color": "#252526",
    "theme": "dark"
  },
  "license": "MIT",
  "homepage": "https://github.com/your-username/nextcode",
  "repository": {
    "type": "git",
    "url": "https://github.com/your-username/nextcode.git"
  },
  "bugs": {
    "url": "https://github.com/your-username/nextcode/issues"
  },
  "qna": "https://github.com/your-username/nextcode/discussions",
  "sponsor": {
    "url": "https://github.com/sponsors/your-username"
  },
  "badges": [
    {
      "url": "https://img.shields.io/badge/license-MIT-blue.svg",
      "href": "https://github.com/your-username/nextcode/blob/main/LICENSE",
      "description": "License"
    }
  ],
  "screenshots": [
    {
      "path": "screenshots/completion.png",
      "title": "Code Completion",
      "description": "Smart AI code suggestions"
    },
    {
      "path": "screenshots/settings.png",
      "title": "Settings",
      "description": "Support multiple Chinese LLM providers"
    }
  ],
  "main": "./out/extension.js",
  "contributes": {
    "configuration": {
      "title": "NextCode",
      "properties": {
        "nextCode.apiProvider": {
          "type": "string",
          "default": "deepseek",
          "enum": [
            "deepseek",
            "qwen",
            "baichuan", 
            "zhipu",
            "minimax",
            "tencent",
            "openai",
            "kimi",
            "custom"
          ],
          "enumDescriptions": [
            "DeepSeek (深度求索)",
            "通义千问 (阿里云)",
            "Baichuan (百川智能)",
            "智谱 AI (GLM)",
            "MiniMax",
            "腾讯混元",
            "OpenAI",
            "Kimi (Moonshot)",
            "Custom API"
          ],
          "description": "Choose AI model provider"
        }
      }
    }
  }
}
```

---

## 📦 打包和发布

### 安装 vsce 工具

```bash
# 全局安装
npm install -g @vscode/vsce

# 或使用 npx（无需全局安装）
npx @vscode/vsce
```

### 登录发布者账户

```bash
# 使用 PAT 登录
vsce login nextcode

# 提示输入 Personal Access Token
# 粘贴之前复制的 token
```

### 打包扩展

```bash
cd nextCode

# 检查 package.json
vsce package --yarn

# 这会生成 nextcode-1.0.0.vsix 文件
```

### 发布到 Marketplace

```bash
# 发布（自动递增版本号）
vsce publish

# 或指定版本号
vsce publish 1.0.0

# 或使用 yarn
vsce publish --yarn
```

### 发布选项

```bash
# 预发布版本（用户需要设置才能安装）
vsce publish --pre-release

# 指定平台
vsce publish --target linux-x64

# 不验证（跳过某些检查）
vsce publish --no-verify
```

---

## 🔄 更新版本

### 自动递增版本

```bash
# 补丁版本 1.0.0 -> 1.0.1
vsce publish patch

# 次要版本 1.0.0 -> 1.1.0
vsce publish minor

# 主要版本 1.0.0 -> 2.0.0
vsce publish major
```

### 手动更新版本

1. 修改 package.json 中的 version
2. 更新 CHANGELOG.md
3. 提交到 git
4. 发布

```bash
git add .
git commit -m "Release v1.0.1"
git tag v1.0.1
git push origin main --tags
vsce publish
```

---

## 📊 发布后管理

### 查看发布状态

访问：https://marketplace.visualstudio.com/items?itemName=nextcode.nextcode

### 更新插件信息

1. 修改 README.md、screenshots 等
2. 重新打包发布

```bash
vsce publish patch
```

### 下架插件

访问 Marketplace 管理页面：
https://marketplace.visualstudio.com/manage/publishers/nextcode

---

## ⚠️ 注意事项

### 常见错误

#### 1. 版本号已存在
```
Error: Version 1.0.0 already exists
```
**解决**: 递增版本号再发布

#### 2. PAT 无效
```
Error: Invalid Personal Access Token
```
**解决**: 
- 检查 token 是否过期
- 确认 token 有 Marketplace Manage 权限
- 重新创建 token

#### 3. 发布者不存在
```
Error: Publisher not found
```
**解决**: 
- 确认已在 Marketplace 创建发布者
- 检查 publisher ID 是否正确

#### 4. 缺少图标
```
Warning: Missing icon
```
**解决**: 确保 icon.png 存在且路径正确

### 最佳实践

1. **测试后再发布**
   ```bash
   # 先本地打包测试
   vsce package
   # 在 VSCode 中安装 .vsix 测试
   ```

2. **更新日志**
   维护 CHANGELOG.md：
   ```markdown
   ## [1.0.1] - 2024-01-28
   ### Fixed
   - 修复 API 请求超时问题
   
   ## [1.0.0] - 2024-01-27
   ### Added
   - 初始版本发布
   ```

3. **Git 标签**
   每次发布打标签：
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

4. **README 优化**
   - 添加 GIF 演示动画
   - 详细的功能说明
   - 清晰的配置指南
   - 常见问题解答

---

## 🚀 推广插件

### 1. GitHub 仓库
- 完善 README
- 添加 badges
- 创建 releases

### 2. 社交媒体
- 知乎、掘金、CSDN 写文章介绍
- Twitter/X 分享
- 开发者社区推广

### 3. SEO 优化
- 关键词：VSCode AI 插件、Copilot 国产替代、代码补全
- 中文关键词：国产大模型、DeepSeek 插件、通义千问 VSCode

---

## 📚 相关链接

- [VSCode Extension API](https://code.visualstudio.com/api)
- [Publishing Extensions](https://code.visualstudio.com/api/working-with-extensions/publishing-extension)
- [Marketplace 管理](https://marketplace.visualstudio.com/manage)
- [Azure DevOps](https://dev.azure.com)

---

## ✅ 发布检查清单

- [ ] 创建 Azure DevOps 账户
- [ ] 创建 Personal Access Token
- [ ] 创建发布者账户
- [ ] 准备 icon.png (256x256)
- [ ] 准备截图 (1200x800)
- [ ] 完善 package.json
- [ ] 完善 README.md
- [ ] 添加 CHANGELOG.md
- [ ] 本地测试通过
- [ ] 打包成功
- [ ] 发布到 Marketplace
- [ ] 验证可搜索和安装
- [ ] 更新 GitHub 仓库

---

**祝发布成功！🎉**