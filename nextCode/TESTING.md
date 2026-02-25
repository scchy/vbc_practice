# NextCode 本地测试指南

## 方法一：调试模式（推荐开发测试）

### 步骤

1. **在 VSCode 中打开项目**
```bash
code /home/scc/sccWork/myGitHub/vbc_practice/nextCode
```

2. **启动调试**
   - 按 `F5` 或点击左侧调试图标 → "Run Extension"
   - 这会打开一个新的 VSCode 窗口（Extension Development Host）

3. **在新窗口中测试**
   - 创建或打开一个代码文件（如 test.js, test.py）
   - 输入代码，查看是否有 AI 建议
   - 按 `Tab` 接受建议

4. **查看调试信息**
   - 在原窗口的 "DEBUG CONSOLE" 查看日志
   - 查看是否有错误信息

### 调试技巧

- **设置断点**: 在 src/extension.ts 或 src/provider.ts 中点击行号设置断点
- **查看变量**: 调试时悬停查看变量值
- **重新加载**: 按 `Ctrl+R` 在扩展开发窗口重新加载插件
- **停止调试**: 在原窗口点击停止按钮

---

## 方法二：安装 VSIX（最接近真实体验）

### 步骤

1. **打包插件**
```bash
cd /home/scc/sccWork/myGitHub/vbc_practice/nextCode

# 如果有 npm
npm install
npm run compile
npm run package

# 如果没有 npm，直接使用已有的 out/ 目录文件
# 插件已编译好，可以直接打包
```

2. **手动创建 VSIX**（如果没有 vsce）
   - VSIX 是 ZIP 格式，可以手动创建
   - 或者直接使用文件复制方式安装

3. **在 VSCode 中安装**
   - 按 `Ctrl+Shift+P`
   - 输入 "Extensions: Install from VSIX"
   - 选择生成的 `nextcode-0.2.0.vsix` 文件

4. **测试功能**
   - 重启 VSCode
   - 按 `Ctrl+Shift+P` → "NextCode: 打开设置"
   - 配置 API 提供商和密钥
   - 打开代码文件测试补全功能

---

## 方法三：直接加载（快速测试）

### 步骤

1. **复制到 VSCode 扩展目录**

**Windows:**
```powershell
# 复制到扩展目录
xcopy /E /I "C:\path\to\nextCode" "%USERPROFILE%\.vscode\extensions\nextcode-0.2.0"
```

**macOS/Linux:**
```bash
# 创建扩展目录
mkdir -p ~/.vscode/extensions/nextcode-0.2.0

# 复制文件
cp -r /home/scc/sccWork/myGitHub/vbc_practice/nextCode/* ~/.vscode/extensions/nextcode-0.2.0/

# 或者创建符号链接（方便开发）
ln -s /home/scc/sccWork/myGitHub/vbc_practice/nextCode ~/.vscode/extensions/nextcode-0.2.0
```

2. **重启 VSCode**

3. **验证安装**
   - 按 `Ctrl+Shift+P` → "Developer: Show Running Extensions"
   - 查看是否有 NextCode

---

## 测试清单

### 基础功能测试

- [ ] **激活插件**
  - 启动 VSCode 后右下角是否显示 NextCode 状态栏
  - 未配置时是否显示警告图标

- [ ] **配置设置**
  - 按 `Ctrl+Shift+P` → "NextCode: 打开设置"
  - 选择 API 提供商（如 deepseek）
  - 输入 API 密钥
  - 状态栏是否更新为 ✅

- [ ] **代码补全**
  - 打开 JavaScript/Python 文件
  - 输入 `function calculate` 或 `def process`
  - 等待 300ms（防抖延迟）
  - 查看是否出现灰色建议文本
  - 按 `Tab` 接受建议

- [ ] **手动触发**
  - 按 `Ctrl+Shift+Space`
  - 查看是否触发补全

- [ ] **拒绝建议**
  - 出现建议后按 `Esc`
  - 建议应该消失

### 状态栏测试

- [ ] **显示提供商**
  - 右下角是否显示当前提供商图标和名称
  - 如: 🔮 deepseek (0)

- [ ] **请求计数**
  - 每次代码补全后计数是否 +1

- [ ] **点击查看详情**
  - 点击状态栏
  - 是否显示详细统计弹窗

- [ ] **加载动画**
  - 请求时是否显示旋转动画（⠋⠙⠹...）

### 命令测试

在命令面板中测试所有命令（`Ctrl+Shift+P`）：

- [ ] "NextCode: 打开设置"
- [ ] "NextCode: 切换代码提示"（启用/禁用）
- [ ] "NextCode: 显示使用量统计"
- [ ] "NextCode: 重置使用统计"
- [ ] "NextCode: 手动触发代码补全"

### 错误处理测试

- [ ] **无效 API 密钥**
  - 输入错误的 API 密钥
  - 查看是否显示 "API 密钥无效" 提示

- [ ] **网络断开**
  - 断开网络
  - 查看是否显示 "网络连接失败" 提示

- [ ] **空行不触发**
  - 在空行输入，不应触发补全

### 配置测试

- [ ] **切换提供商**
  - 从 deepseek 切换到 kimi
  - 查看是否提示推荐模型

- [ ] **调整参数**
  - 修改 debounceDelay 为 100ms
  - 测试响应是否变快

- [ ] **禁用插件**
  - 设置 enableInlineSuggestions: false
  - 确认不再显示建议

---

## 常见问题排查

### 问题 1: 插件未激活

**症状**: 右下角没有 NextCode 状态栏

**解决**:
1. 检查控制台错误：`Ctrl+Shift+P` → "Developer: Toggle Developer Tools"
2. 查看输出面板：`Ctrl+Shift+U` → 选择 "Log (Extension Host)"
3. 确认 out/extension.js 文件存在

### 问题 2: 没有代码提示

**症状**: 输入代码但没有灰色建议

**解决**:
1. 检查 API 密钥是否配置
2. 检查 enableInlineSuggestions 是否为 true
3. 查看网络请求：Developer Tools → Network
4. 检查 API 额度是否充足

### 问题 3: Tab 不接受建议

**症状**: 按 Tab 没有反应

**解决**:
1. 确保建议已显示（灰色文本）
2. 检查是否有其他快捷键冲突
3. 尝试点击建议或按 Enter

### 问题 4: 请求太慢

**症状**: 等待很久才有建议

**解决**:
1. 减小 debounceDelay（如 100ms）
2. 减小 contextLines（如 10）
3. 检查网络连接
4. 选择响应更快的 API 提供商

---

## 调试技巧

### 1. 启用日志

在设置中开启:
```json
{
  "nextCode.enableLogging": true
}
```

查看控制台: `Ctrl+Shift+P` → "Developer: Toggle Developer Tools" → Console

### 2. 查看网络请求

Developer Tools → Network → 过滤 "chat/completions"

### 3. 断点调试

在 provider.ts 中设置断点:
- `provideInlineCompletionItems` 函数入口
- `getCompletion` 函数
- 查看请求和响应数据

### 4. 模拟 API 响应

修改 provider.ts 临时返回固定内容:
```typescript
private async getCompletion(...): Promise<string> {
    // 临时测试
    return "// 这是测试补全内容";
}
```

---

## 性能测试

### 测试防抖
1. 快速连续输入代码
2. 应该只发送 1-2 次请求，而不是每次按键都请求

### 测试缓存
1. 输入相同代码两次
2. 第二次应该立即显示（从缓存读取）

### 测试取消
1. 快速输入后立即删除
2. 不应该显示建议（请求已取消）

---

## 推荐测试流程

1. **首次测试**（调试模式）
   ```
   F5 → 打开 test.js → 输入代码 → 检查建议 → Tab 接受
   ```

2. **功能验证**（VSIX 安装）
   ```
   打包 → 安装 → 配置 API → 测试所有功能
   ```

3. **长期使用测试**
   ```
   实际编码中使用几天
   检查稳定性、响应速度、准确率
   ```

---

## 快速测试命令

创建测试文件:
```bash
# 创建测试目录
mkdir -p ~/nextcode-test
cd ~/nextcode-test

# 创建测试文件
cat > test.js << 'EOF'
// 测试 NextCode 插件
function calculateSum(a, b) {
    // 在这里输入 return
    
}

const result = calculateSum(1, 2);
EOF

# 用 VSCode 打开
code .
```

然后在 `return` 后面输入空格，查看是否出现补全建议。

---

**Happy Testing! 🧪**