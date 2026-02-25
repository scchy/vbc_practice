import * as vscode from 'vscode';

export interface NextCodeConfig {
    apiProvider: string;
    apiKey: string;
    apiEndpoint: string;
    model: string;
    maxTokens: number;
    temperature: number;
    enableInlineSuggestions: boolean;
    showUsage: boolean;
    debounceDelay: number;
    contextLines: number;
    enableLogging: boolean;
}

// 模型配置映射
export const MODEL_CONFIGS: Record<string, { defaultModel: string; maxTokens: number; supportsStreaming: boolean }> = {
    'deepseek': { defaultModel: 'deepseek-chat', maxTokens: 4096, supportsStreaming: true },
    'qwen': { defaultModel: 'qwen-turbo', maxTokens: 8192, supportsStreaming: true },
    'baichuan': { defaultModel: 'Baichuan2-Turbo', maxTokens: 4096, supportsStreaming: true },
    'zhipu': { defaultModel: 'glm-4', maxTokens: 8192, supportsStreaming: true },
    'minimax': { defaultModel: 'abab6.5-chat', maxTokens: 8192, supportsStreaming: true },
    'tencent': { defaultModel: 'hunyuan-lite', maxTokens: 4096, supportsStreaming: false },
    'openai': { defaultModel: 'gpt-3.5-turbo', maxTokens: 4096, supportsStreaming: true },
    'kimi': { defaultModel: 'moonshot-v1-8k', maxTokens: 8192, supportsStreaming: true },
    'custom': { defaultModel: 'default', maxTokens: 4096, supportsStreaming: true }
};

export class SettingsManager {
    private config: NextCodeConfig;

    constructor() {
        this.config = this.loadConfig();
    }

    private loadConfig(): NextCodeConfig {
        const config = vscode.workspace.getConfiguration('nextCode');
        return {
            apiProvider: config.get('apiProvider', 'deepseek'),
            apiKey: config.get('apiKey', ''),
            apiEndpoint: config.get('apiEndpoint', ''),
            model: config.get('model', 'deepseek-chat'),
            maxTokens: config.get('maxTokens', 100),
            temperature: config.get('temperature', 0.7),
            enableInlineSuggestions: config.get('enableInlineSuggestions', true),
            showUsage: config.get('showUsage', true),
            debounceDelay: config.get('debounceDelay', 300),
            contextLines: config.get('contextLines', 20),
            enableLogging: config.get('enableLogging', false)
        };
    }

    public getConfig(): NextCodeConfig {
        return this.config;
    }

    public refreshConfig(): void {
        this.config = this.loadConfig();
    }

    public isValid(): boolean {
        if (!this.config.apiKey) {
            return false;
        }
        
        if (this.config.apiProvider === 'custom' && !this.config.apiEndpoint) {
            return false;
        }

        return true;
    }

    public getApiEndpoint(): string {
        const provider = this.config.apiProvider;
        
        // 国产大模型 API 端点
        const endpoints: Record<string, string> = {
            'deepseek': 'https://api.deepseek.com/v1/chat/completions',
            'qwen': 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
            'baichuan': 'https://api.baichuan-ai.com/v1/chat/completions',
            'zhipu': 'https://open.bigmodel.cn/api/paas/v4/chat/completions',
            'minimax': 'https://api.minimax.chat/v1/text/chatcompletion',
            'tencent': 'https://hunyuan.cloud.tencent.com/v1/chat/completions',
            'openai': 'https://api.openai.com/v1/chat/completions',
            'kimi': 'https://api.moonshot.cn/v1/chat/completions'
        };

        if (provider === 'custom') {
            return this.config.apiEndpoint;
        }

        return endpoints[provider] || endpoints.deepseek;
    }

    public getHeaders(): Record<string, string> {
        const apiKey = this.config.apiKey;

        // 所有提供商都使用标准 OpenAI 格式
        return {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json'
        };
    }

    // 获取当前提供商的模型配置
    public getModelConfig() {
        return MODEL_CONFIGS[this.config.apiProvider] || MODEL_CONFIGS.deepseek;
    }

    // 自动设置推荐模型
    public static getRecommendedModel(provider: string): string {
        return MODEL_CONFIGS[provider]?.defaultModel || 'deepseek-chat';
    }

    // 日志记录
    public log(message: string, ...args: any[]): void {
        if (this.config.enableLogging) {
            console.log(`[NextCode] ${message}`, ...args);
        }
    }
}