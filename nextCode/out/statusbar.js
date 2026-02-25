"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.StatusBarManager = void 0;
const vscode = __importStar(require("vscode"));
class StatusBarManager {
    constructor() {
        this.usageStats = {
            requestCount: 0,
            tokenCount: 0,
            successCount: 0,
            errorCount: 0,
            lastRequestTime: null
        };
        this.isLoading = false;
        this.loadingAnimation = null;
        this.loadingFrames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];
        this.loadingIndex = 0;
        this.statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
        this.statusBarItem.command = 'nextCode.showUsage';
        this.updateTooltip();
    }
    updateStatusBar() {
        const config = vscode.workspace.getConfiguration('nextCode');
        const showUsage = config.get('showUsage', true);
        if (!showUsage) {
            this.statusBarItem.hide();
            return;
        }
        const provider = config.get('apiProvider', 'deepseek');
        const isConfigured = config.get('apiKey', '').length > 0;
        if (this.isLoading) {
            this.statusBarItem.text = `${this.loadingFrames[this.loadingIndex]} NextCode`;
            this.statusBarItem.backgroundColor = undefined;
        }
        else if (!isConfigured) {
            this.statusBarItem.text = `$(warning) NextCode`;
            this.statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');
        }
        else {
            const providerEmoji = this.getProviderEmoji(provider);
            this.statusBarItem.text = `${providerEmoji} ${provider} (${this.usageStats.requestCount})`;
            this.statusBarItem.backgroundColor = undefined;
        }
        this.updateTooltip();
        this.statusBarItem.show();
    }
    getProviderEmoji(provider) {
        const emojis = {
            'deepseek': '🔮',
            'qwen': '🌟',
            'baichuan': '🏔️',
            'zhipu': '🧠',
            'minimax': '🎭',
            'tencent': '🐧',
            'openai': '🤖',
            'kimi': '🌙',
            'custom': '⚙️'
        };
        return emojis[provider] || '🤖';
    }
    updateTooltip() {
        const config = vscode.workspace.getConfiguration('nextCode');
        const provider = config.get('apiProvider', 'deepseek');
        const model = config.get('model', 'default');
        let tooltip = `NextCode AI 代码助手
━━━━━━━━━━━━━━━━
提供商: ${provider}
模型: ${model}`;
        if (this.usageStats.requestCount > 0) {
            tooltip += `
━━━━━━━━━━━━━━━━
请求次数: ${this.usageStats.requestCount}
成功: ${this.usageStats.successCount}
失败: ${this.usageStats.errorCount}
Token 数: ${Math.round(this.usageStats.tokenCount)}`;
            if (this.usageStats.lastRequestTime) {
                const lastTime = new Date(this.usageStats.lastRequestTime).toLocaleTimeString();
                tooltip += `\n最后请求: ${lastTime}`;
            }
        }
        tooltip += '\n━━━━━━━━━━━━━━━━\n点击查看详细信息';
        this.statusBarItem.tooltip = tooltip;
    }
    setLoading(loading) {
        this.isLoading = loading;
        if (loading) {
            // 启动加载动画
            this.loadingAnimation = setInterval(() => {
                this.loadingIndex = (this.loadingIndex + 1) % this.loadingFrames.length;
                this.updateStatusBar();
            }, 100);
        }
        else {
            // 停止加载动画
            if (this.loadingAnimation) {
                clearInterval(this.loadingAnimation);
                this.loadingAnimation = null;
            }
            this.loadingIndex = 0;
        }
        this.updateStatusBar();
    }
    incrementUsage(tokens = 0, success = true) {
        this.usageStats.requestCount++;
        this.usageStats.tokenCount += tokens;
        this.usageStats.lastRequestTime = Date.now();
        if (success) {
            this.usageStats.successCount++;
        }
        else {
            this.usageStats.errorCount++;
        }
        this.updateStatusBar();
    }
    recordError() {
        this.usageStats.errorCount++;
        this.updateStatusBar();
    }
    showUsageDetails() {
        const config = vscode.workspace.getConfiguration('nextCode');
        const provider = config.get('apiProvider', 'deepseek');
        const isConfigured = config.get('apiKey', '').length > 0;
        if (!isConfigured) {
            vscode.window.showWarningMessage('NextCode 未配置 API 密钥', '打开设置', '查看文档').then(selection => {
                if (selection === '打开设置') {
                    vscode.commands.executeCommand('nextCode.openSettings');
                }
                else if (selection === '查看文档') {
                    vscode.env.openExternal(vscode.Uri.parse('https://github.com/your-repo/nextcode'));
                }
            });
            return;
        }
        const model = config.get('model', 'default');
        const successRate = this.usageStats.requestCount > 0
            ? ((this.usageStats.successCount / this.usageStats.requestCount) * 100).toFixed(1)
            : '0.0';
        const message = `
📊 NextCode 使用统计
━━━━━━━━━━━━━━━━━━━━
🔧 提供商: ${provider}
🤖 模型: ${model}
📈 请求次数: ${this.usageStats.requestCount}
✅ 成功: ${this.usageStats.successCount}
❌ 失败: ${this.usageStats.errorCount}
🎯 成功率: ${successRate}%
📝 Token 总数: ${Math.round(this.usageStats.tokenCount)}
━━━━━━━━━━━━━━━━━━━━
        `.trim();
        vscode.window.showInformationMessage(message, { modal: true });
    }
    resetUsage() {
        this.usageStats = {
            requestCount: 0,
            tokenCount: 0,
            successCount: 0,
            errorCount: 0,
            lastRequestTime: null
        };
        this.updateStatusBar();
        vscode.window.showInformationMessage('NextCode 使用统计已重置');
    }
    getStats() {
        return { ...this.usageStats };
    }
    dispose() {
        if (this.loadingAnimation) {
            clearInterval(this.loadingAnimation);
        }
        this.statusBarItem.dispose();
    }
}
exports.StatusBarManager = StatusBarManager;
//# sourceMappingURL=statusbar.js.map