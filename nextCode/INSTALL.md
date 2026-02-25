# NextCode 安装指南

## 完整安装步骤

### 1. 安装 Node.js 和 npm
确保系统已安装 Node.js (v16+) 和 npm。

### 2. 安装依赖
```bash
cd nextCode
npm install
```

### 3. 编译 TypeScript
```bash
npm run compile
```

### 4. 安装 vsce（Visual Studio Code 扩展管理器）
```bash
npm install -g @vscode/vsce
```

### 5. 打包插件
```bash
npm run package
# 或
vsce package
```

### 6. 安装插件
1. 在 VSCode 中按 `Ctrl+Shift+P`
2. 输入 "Extensions: Install from VSIX"
3. 选择生成的 `nextcode-0.1.0.vsix` 文件

## 快速安装（简化版）

如果遇到依赖问题，可以使用简化版本：

```bash
cd nextCode
chmod +x build.sh
./build.sh
```

简化版本会创建一个基本可用的扩展，但缺少完整的 AI 功能。

## 配置 API 密钥

安装后，按 `Ctrl+Shift+P` 搜索 "NextCode: 打开设置"，配置以下内容：

1. **API 提供商**: 选择您使用的服务（如 deepseek、qwen 等）
2. **API 密钥**: 输入从对应平台获取的 API 密钥
3. **模型**: 选择模型名称（如 deepseek-chat、qwen-turbo 等）

## 验证安装

1. 重启 VSCode
2. 查看右下角状态栏是否有 NextCode 图标
3. 尝试输入代码，查看是否出现 AI 建议
4. 按 `Tab` 键测试接受建议功能

## 故障排除

### 常见问题

**Q: 没有代码提示**
A: 检查 API 密钥是否正确，网络是否正常。

**Q: 状态栏不显示**
A: 在设置中启用 `nextCode.showUsage`。

**Q: TypeScript 编译错误**
A: 确保安装了所有依赖：`npm install`

**Q: vsce 命令不存在**
A: 全局安装 vsce：`npm install -g @vscode/vsce`

### 获取帮助
- 查看 VSCode 输出面板中的 NextCode 日志
- 检查控制台错误信息
- 参考 README.md 中的详细说明