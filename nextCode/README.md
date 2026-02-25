# NextCode - AI 代码补全插件

NextCode 是一个类似 Copilot 的 VSCode 插件，支持所有国产大模型 API，提供智能代码生成和补全功能。

## ✨ 功能特性

- 🤖 **多模型支持**: 支持 DeepSeek、通义千问、百度文心、智谱 GLM、MiniMax、腾讯混元、Kimi 等国产大模型
- ⚡ **智能补全**: 根据上下文智能生成代码建议
- 🎯 **防抖优化**: 智能防抖机制，避免频繁请求
- 💾 **响应缓存**: 30 秒缓存机制，提升响应速度
- ⌨️ **Tab 接受**: 使用 Tab 键快速接受建议
- 📊 **使用量显示**: 右下角状态栏显示请求次数、Token 使用量和成功率
- 🎨 **加载动画**: 请求时显示加载动画
- ⚙️ **简单配置**: 类似 Roo Code 的设置页面，只需配置 API 密钥
- 🔒 **隐私保护**: 所有请求直接发送到您选择的 API 提供商
- 📝 **详细统计**: 成功率、错误率、Token 使用量统计

## 🚀 快速开始

### 安装

#### 从 VSIX 安装
1. 下载 `nextcode-0.2.0.vsix` 文件
2. 在 VSCode 中按 `Ctrl+Shift+P`，输入 "Extensions: Install from VSIX"
3. 选择下载的 VSIX 文件

#### 从源码构建
```bash
cd nextCode
npm install
npm run compile
npm run package
```

### 配置

1. 安装插件后，按 `Ctrl+Shift+P` 搜索 "NextCode: 打开设置"
2. 在设置页面中：
   - **API 提供商**: 选择 AI 模型提供商（如 deepseek、qwen、zhipu、kimi 等）
   - **API 密钥**: 输入从对应平台获取的 API 密钥
   - **模型**: 选择模型名称（插件会自动推荐适合的模型）
   - **高级设置**: 调整温度、最大 Token 数、防抖延迟等参数

### 支持的 API 提供商

| 提供商 | 默认模型 | 最大 Token | 流式支持 |
|--------|----------|------------|----------|
| **DeepSeek** | deepseek-chat | 4096 | ✅ |
| **通义千问** | qwen-turbo | 8192 | ✅ |
| **智谱 AI** | glm-4 | 8192 | ✅ |
| **Baichuan** | Baichuan2-Turbo | 4096 | ✅ |
| **MiniMax** | abab6.5-chat | 8192 | ✅ |
| **腾讯混元** | hunyuan-lite | 4096 | ❌ |
| **Kimi** | moonshot-v1-8k | 8192 | ✅ |
| **OpenAI** | gpt-3.5-turbo | 4096 | ✅ |
| **自定义** | - | 4096 | ✅ |

### 平台注册链接

- **DeepSeek**: https://platform.deepseek.com/
- **通义千问**: https://dashscope.aliyun.com/
- **智谱 AI**: https://open.bigmodel.cn/
- **Baichuan**: https://platform.baichuan-ai.com/
- **MiniMax**: https://api.minimax.chat/
- **腾讯混元**: https://cloud.tencent.com/product/hunyuan
- **Kimi**: https://platform.moonshot.cn/
- **OpenAI**: https://platform.openai.com/

## 🎯 使用方法

### 代码补全
1. 在编辑器中输入代码
2. NextCode 会自动分析上下文并生成建议（灰色文本）
3. 按 `Tab` 键接受建议
4. 按 `Esc` 键拒绝建议

### 手动触发
- 按 `Ctrl+Shift+Space` 手动触发代码补全
- 或右键菜单选择 "NextCode: 手动触发代码补全"

### 状态栏
- 右下角显示当前使用的提供商和请求次数
- 🔮 DeepSeek, 🌟 通义千问, 🧠 智谱, 🌙 Kimi 等图标
- 点击状态栏查看详细使用统计
- 加载时显示旋转动画

### 命令面板
按 `Ctrl+Shift+P` 搜索：

| 命令 | 功能 |
|------|------|
| `NextCode: 打开设置` | 打开插件设置 |
| `NextCode: 在侧边栏打开设置` | 在侧边栏打开设置 |
| `NextCode: 切换代码提示` | 启用/禁用代码提示 |
| `NextCode: 显示使用量统计` | 显示详细使用统计 |
| `NextCode: 重置使用统计` | 重置统计数据 |
| `NextCode: 手动触发代码补全` | 手动触发补全 |
| `NextCode: 接受当前建议` | 接受当前建议 |
| `NextCode: 拒绝当前建议` | 拒绝当前建议 |

## ⚙️ 高级配置

在 VSCode 设置中搜索 "NextCode"：

```json
{
  "nextCode.apiProvider": "deepseek",
  "nextCode.apiKey": "your-api-key",
  "nextCode.model": "deepseek-chat",
  "nextCode.maxTokens": 100,
  "nextCode.temperature": 0.7,
  "nextCode.enableInlineSuggestions": true,
  "nextCode.showUsage": true,
  "nextCode.debounceDelay": 300,
  "nextCode.contextLines": 20,
  "nextCode.enableLogging": false
}
```

### 配置说明

- **debounceDelay**: 防抖延迟（100-2000ms），避免频繁请求
- **contextLines**: 上下文行数（5-50），影响代码理解准确度
- **enableLogging**: 启用调试日志，查看控制台输出
- **temperature**: 生成温度（0-2），越高越随机
- **maxTokens**: 生成的最大 Token 数（10-4096）

## 🛠️ 开发

### 项目结构
```
nextCode/
├── src/
│   ├── extension.ts      # 插件入口点
│   ├── provider.ts       # 代码补全提供程序（核心逻辑）
│   ├── settings.ts       # 配置管理
│   └── statusbar.ts      # 状态栏管理
├── out/                  # 编译后的 JavaScript
├── package.json          # 插件清单
├── tsconfig.json         # TypeScript 配置
├── README.md             # 本文档
├── INSTALL.md            # 安装指南
└── build.sh              # 构建脚本
```

### 核心功能实现

#### 智能防抖
- 可配置的防抖延迟（默认 300ms）
- 避免用户快速输入时频繁请求

#### 响应缓存
- 30 秒缓存机制
- 基于上下文的哈希缓存
- 提升重复代码的响应速度

#### 上下文提取
- 智能提取前 N 行代码作为上下文
- 过滤空行和特殊字符行
- 添加文件类型信息

#### 错误处理
- 网络错误检测和提示
- API 密钥无效提示
- 请求频率限制处理
- 服务不可用提示

### 构建和测试

```bash
# 安装依赖
npm install

# 编译 TypeScript
npm run compile

# 监视模式
npm run watch

# 运行测试
npm test

# 打包插件
npm run package
```

### 调试

1. 在 VSCode 中打开项目
2. 按 `F5` 启动调试
3. 在新窗口中测试插件功能
4. 查看调试控制台输出

## 🐛 故障排除

### 常见问题

**Q: 没有代码提示**
```
A: 1. 检查 API 密钥是否正确配置
   2. 确认网络连接正常
   3. 查看 VSCode 输出面板中的 NextCode 日志
   4. 确保 enableInlineSuggestions 设置为 true
```

**Q: 状态栏显示 "未配置"**
```
A: 1. 打开设置 (Ctrl+Shift+P → NextCode: 打开设置)
   2. 配置 apiProvider 和 apiKey
   3. 重启 VSCode
```

**Q: API 请求失败**
```
A: 1. 检查 API 密钥是否正确
   2. 确认 API 端点可访问
   3. 查看错误信息并调整配置
   4. 检查是否超出 API 调用限制
```

**Q: 补全质量不高**
```
A: 1. 调整 temperature 参数（0.3-0.7 适合代码补全）
   2. 增加 contextLines 以获取更多上下文
   3. 尝试不同的模型
```

### 日志查看

在 VSCode 中：
1. 打开输出面板 `Ctrl+Shift+U`
2. 选择 "NextCode" 查看详细日志
3. 或启用 `nextCode.enableLogging` 查看控制台输出

### 性能优化

如果插件响应慢：
1. 降低 `debounceDelay` 到 100-200ms
2. 减少 `contextLines` 到 10-15 行
3. 降低 `maxTokens` 到 50-100
4. 确保网络连接稳定

## 📋 更新日志

### v0.2.0 (优化版本)
- ✨ 添加智能防抖机制
- 💾 添加响应缓存（30秒）
- 🎨 添加状态栏加载动画
- 📊 增强使用量统计（成功率、错误率）
- 🔧 添加模型自动推荐功能
- ⌨️ 添加快捷键绑定（Ctrl+Shift+Space）
- 🛠️ 优化错误处理和提示
- 📝 改进上下文提取算法
- 🎯 添加更多代码语言支持

### v0.1.0 (初始版本)
- 🎉 初始版本发布
- 🤖 支持主流国产大模型 API
- 💡 实现代码补全和 Tab 接受功能
- 📊 添加状态栏使用量显示
- ⚙️ 提供简单易用的设置页面

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献指南
1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📞 联系方式

- GitHub Issues: https://github.com/your-username/nextcode/issues
- Email: your-email@example.com

---

**Enjoy coding with NextCode! 🚀**