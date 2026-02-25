import * as vscode from 'vscode';

export interface UsageStats {
    requestCount: number;
    tokenCount: number;
    successCount: number;
    errorCount: number;
    lastRequestTime: number | null;
}

export class StatusBarManager implements vscode.Disposable {
    private statusBarItem: vscode.StatusBarItem;
    private usageStats: UsageStats = {
        requestCount: 0,
        tokenCount: 0,
        successCount: 0,
        errorCount: 0,
        lastRequestTime: null
    };
    private isLoading: boolean = false;
    private loadingAnimation: NodeJS.Timeout | null = null;
    private loadingFrames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];
    private loadingIndex = 0;

    constructor() {
        this.statusBarItem = vscode.window.createStatusBarItem(
            vscode.StatusBarAlignment.Right,
            100
        );
        this.statusBarItem.command = 'nextCode.showUsage';
        this.updateTooltip();
    }

    public updateStatusBar(): void {
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
        } else if (!isConfigured) {
            this.statusBarItem.text = `$(warning) NextCode`;
            this.statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');
        } else {
            const providerEmoji = this.getProviderEmoji(provider);
            this.statusBarItem.text = `${providerEmoji} ${provider} (${this.usageStats.requestCount})`;
            this.statusBarItem.backgroundColor = undefined;
        }

        this.updateTooltip();
        this.statusBarItem.show();
    }

    private getProviderEmoji(provider: string): string {
        const emojis: Record<string, string> = {
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

    private updateTooltip(): void {
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

    public setLoading(loading: boolean): void {
        this.isLoading = loading;
        
        if (loading) {
            // 启动加载动画
            this.loadingAnimation = setInterval(() => {
                this.loadingIndex = (this.loadingIndex + 1) % this.loadingFrames.length;
                this.updateStatusBar();
            }, 100);
        } else {
            // 停止加载动画
            if (this.loadingAnimation) {
                clearInterval(this.loadingAnimation);
                this.loadingAnimation = null;
            }
            this.loadingIndex = 0;
        }
        
        this.updateStatusBar();
    }

    public incrementUsage(tokens: number = 0, success: boolean = true): void {
        this.usageStats.requestCount++;
        this.usageStats.tokenCount += tokens;
        this.usageStats.lastRequestTime = Date.now();
        
        if (success) {
            this.usageStats.successCount++;
        } else {
            this.usageStats.errorCount++;
        }
        
        this.updateStatusBar();
    }

    public recordError(): void {
        this.usageStats.errorCount++;
        this.updateStatusBar();
    }

    public showUsageDetails(): void {
        const config = vscode.workspace.getConfiguration('nextCode');
        const provider = config.get('apiProvider', 'deepseek');
        const isConfigured = config.get('apiKey', '').length > 0;

        if (!isConfigured) {
            vscode.window.showWarningMessage(
                'NextCode 未配置 API 密钥',
                '打开设置',
                '查看文档'
            ).then(selection => {
                if (selection === '打开设置') {
                    vscode.commands.executeCommand('nextCode.openSettings');
                } else if (selection === '查看文档') {
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

    public resetUsage(): void {
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

    public getStats(): UsageStats {
        return { ...this.usageStats };
    }

    public dispose(): void {
        if (this.loadingAnimation) {
            clearInterval(this.loadingAnimation);
        }
        this.statusBarItem.dispose();
    }
}