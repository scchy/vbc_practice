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
exports.SettingsManager = exports.MODEL_CONFIGS = void 0;
const vscode = __importStar(require("vscode"));
// 模型配置映射
exports.MODEL_CONFIGS = {
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
class SettingsManager {
    constructor() {
        this.config = this.loadConfig();
    }
    loadConfig() {
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
    getConfig() {
        return this.config;
    }
    refreshConfig() {
        this.config = this.loadConfig();
    }
    isValid() {
        if (!this.config.apiKey) {
            return false;
        }
        if (this.config.apiProvider === 'custom' && !this.config.apiEndpoint) {
            return false;
        }
        return true;
    }
    getApiEndpoint() {
        const provider = this.config.apiProvider;
        // 国产大模型 API 端点
        const endpoints = {
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
    getHeaders() {
        const apiKey = this.config.apiKey;
        // 所有提供商都使用标准 OpenAI 格式
        return {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json'
        };
    }
    // 获取当前提供商的模型配置
    getModelConfig() {
        return exports.MODEL_CONFIGS[this.config.apiProvider] || exports.MODEL_CONFIGS.deepseek;
    }
    // 自动设置推荐模型
    static getRecommendedModel(provider) {
        return exports.MODEL_CONFIGS[provider]?.defaultModel || 'deepseek-chat';
    }
    // 日志记录
    log(message, ...args) {
        if (this.config.enableLogging) {
            console.log(`[NextCode] ${message}`, ...args);
        }
    }
}
exports.SettingsManager = SettingsManager;
//# sourceMappingURL=settings.js.map