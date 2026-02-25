import * as vscode from 'vscode';
import axios from 'axios';
import { SettingsManager } from './settings';
import { statusBarManager } from './extension';

export class NextCodeProvider implements vscode.InlineCompletionItemProvider, vscode.Disposable {
    private settingsManager: SettingsManager;
    private isEnabled: boolean = true;
    private pendingRequest: AbortController | null = null;
    private debounceTimer: NodeJS.Timeout | null = null;
    private lastCompletionTime: number = 0;
    private cache: Map<string, { completion: string; timestamp: number }> = new Map();
    private readonly CACHE_TTL = 30000; // 30秒缓存

    constructor() {
        this.settingsManager = new SettingsManager();
    }

    public async provideInlineCompletionItems(
        document: vscode.TextDocument,
        position: vscode.Position,
        context: vscode.InlineCompletionContext,
        token: vscode.CancellationToken
    ): Promise<vscode.InlineCompletionItem[] | vscode.InlineCompletionList | null> {
        // 检查是否启用
        if (!this.isEnabled || !this.settingsManager.getConfig().enableInlineSuggestions) {
            return null;
        }

        // 检查是否有有效的配置
        if (!this.settingsManager.isValid()) {
            this.settingsManager.log('配置无效，跳过代码补全');
            return null;
        }

        // 防抖处理
        const config = this.settingsManager.getConfig();
        const now = Date.now();
        const timeSinceLastCompletion = now - this.lastCompletionTime;
        
        if (timeSinceLastCompletion < config.debounceDelay) {
            this.settingsManager.log('防抖：跳过快速触发');
            return null;
        }

        // 获取上下文信息
        const contextInfo = this.extractContext(document, position);
        if (!contextInfo.shouldComplete) {
            return null;
        }

        // 检查缓存
        const cacheKey = contextInfo.contextHash;
        const cached = this.cache.get(cacheKey);
        if (cached && (now - cached.timestamp < this.CACHE_TTL)) {
            this.settingsManager.log('使用缓存的补全结果');
            return this.createCompletionItems(cached.completion, position);
        }

        // 取消之前的请求
        if (this.pendingRequest) {
            this.pendingRequest.abort();
            this.pendingRequest = null;
        }

        if (this.debounceTimer) {
            clearTimeout(this.debounceTimer);
        }

        // 返回 Promise，实现异步补全
        return new Promise((resolve) => {
            this.debounceTimer = setTimeout(async () => {
                if (token.isCancellationRequested) {
                    resolve(null);
                    return;
                }

                try {
                    const controller = new AbortController();
                    this.pendingRequest = controller;

                    const completion = await this.getCompletion(
                        contextInfo.contextText, 
                        document.languageId,
                        controller.signal
                    );
                    
                    if (token.isCancellationRequested || !completion) {
                        resolve(null);
                        return;
                    }

                    // 缓存结果
                    this.cache.set(cacheKey, { completion, timestamp: Date.now() });
                    
                    // 更新使用统计
                    statusBarManager.incrementUsage(completion.length / 4);
                    this.lastCompletionTime = Date.now();

                    resolve(this.createCompletionItems(completion, position));
                } catch (error: any) {
                    this.handleError(error);
                    resolve(null);
                } finally {
                    this.pendingRequest = null;
                }
            }, config.debounceDelay);
        });
    }

    private extractContext(
        document: vscode.TextDocument, 
        position: vscode.Position
    ): { contextText: string; contextHash: string; shouldComplete: boolean } {
        const config = this.settingsManager.getConfig();
        const line = document.lineAt(position.line);
        const lineText = line.text.substring(0, position.character);
        
        // 智能判断是否应该提供补全
        const trimmedLine = lineText.trim();
        
        // 如果当前行只有空格或特殊字符，不提供补全
        if (trimmedLine.length === 0 || /^[\s\{\}\[\]\(\)]+$/.test(trimmedLine)) {
            return { contextText: '', contextHash: '', shouldComplete: false };
        }

        // 获取更智能的上下文
        const startLine = Math.max(0, position.line - config.contextLines);
        let contextText = '';
        
        // 添加文件类型信息
        contextText += `// Language: ${document.languageId}\n`;
        
        // 添加上下文
        for (let i = startLine; i < position.line; i++) {
            contextText += document.lineAt(i).text + '\n';
        }
        contextText += lineText;

        // 创建简单的哈希用于缓存
        const contextHash = this.simpleHash(contextText);

        return { contextText, contextHash, shouldComplete: true };
    }

    private simpleHash(str: string): string {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return hash.toString(16);
    }

    private createCompletionItems(
        completion: string, 
        position: vscode.Position
    ): vscode.InlineCompletionItem[] {
        const item = new vscode.InlineCompletionItem(
            completion,
            new vscode.Range(position, position)
        );
        
        // 不设置 command，让 VSCode 默认处理 Tab 接受
        // 用户可以直接按 Tab 接受建议
        
        return [item];
    }

    private async getCompletion(
        prompt: string, 
        languageId: string,
        signal: AbortSignal
    ): Promise<string> {
        const config = this.settingsManager.getConfig();
        const modelConfig = this.settingsManager.getModelConfig();
        
        // 构建更智能的提示
        const systemPrompt = `You are an expert code completion assistant. 
Your task is to provide concise, contextually appropriate code completions.
- Complete the code based on the given context
- Return ONLY the completion code, no explanations
- Ensure the code is syntactically correct for ${languageId}
- Keep completions short and focused (1-3 lines preferred)`;

        const requestBody: any = {
            model: config.model,
            messages: [
                { role: 'system', content: systemPrompt },
                { 
                    role: 'user', 
                    content: `Complete this ${languageId} code:\n\`\`\`${languageId}\n${prompt}\n\`\`\`` 
                }
            ],
            max_tokens: Math.min(config.maxTokens, modelConfig.maxTokens),
            temperature: config.temperature,
            stream: false,
            stop: ['\n\n', '\r\n\r\n'] // 防止生成过多内容
        };

        try {
            this.settingsManager.log('发送请求到 API...');
            
            const response = await axios.post(
                this.settingsManager.getApiEndpoint(),
                requestBody,
                {
                    headers: this.settingsManager.getHeaders(),
                    signal,
                    timeout: 8000 // 8秒超时
                }
            );

            // 解析响应
            let completion = this.parseResponse(response.data, config.apiProvider);
            
            // 清理响应
            completion = this.cleanCompletion(completion, prompt);
            
            this.settingsManager.log('收到补全结果:', completion.substring(0, 50) + '...');
            
            return completion;
        } catch (error: any) {
            throw error;
        }
    }

    private parseResponse(data: any, provider: string): string {
        // 统一的响应解析
        let completion = '';
        
        if (data.choices && data.choices[0]) {
            if (data.choices[0].message && data.choices[0].message.content) {
                completion = data.choices[0].message.content;
            } else if (data.choices[0].text) {
                completion = data.choices[0].text;
            }
        } else if (data.output && data.output.text) {
            // 通义千问特殊格式
            completion = data.output.text;
        }

        return completion || '';
    }

    private cleanCompletion(completion: string, context: string): string {
        let cleaned = completion.trim();
        
        // 移除代码块标记
        if (cleaned.startsWith('```')) {
            const lines = cleaned.split('\n');
            if (lines[0].startsWith('```')) {
                lines.shift();
            }
            if (lines.length > 0 && lines[lines.length - 1].startsWith('```')) {
                lines.pop();
            }
            cleaned = lines.join('\n').trim();
        }

        // 如果补全内容已经在上下文中，跳过
        if (context.trim().endsWith(cleaned.trim())) {
            return '';
        }

        // 限制长度
        const maxLength = 200;
        if (cleaned.length > maxLength) {
            cleaned = cleaned.substring(0, maxLength);
            // 尝试在合理的边界截断
            const lastNewline = cleaned.lastIndexOf('\n');
            if (lastNewline > maxLength * 0.7) {
                cleaned = cleaned.substring(0, lastNewline);
            }
        }

        return cleaned;
    }

    private handleError(error: any): void {
        if (error.name === 'AbortError') {
            this.settingsManager.log('请求被取消');
            return;
        }
        
        console.error('NextCode 错误:', error);
        
        if (error.response) {
            switch (error.response.status) {
                case 401:
                    vscode.window.showErrorMessage('NextCode: API 密钥无效');
                    break;
                case 429:
                    vscode.window.showWarningMessage('NextCode: 请求过于频繁');
                    break;
                case 500:
                case 502:
                case 503:
                    vscode.window.showWarningMessage('NextCode: 服务暂时不可用');
                    break;
                default:
                    this.settingsManager.log(`API 错误: ${error.response.status}`);
            }
        } else if (error.code === 'ENOTFOUND' || error.code === 'ECONNREFUSED') {
            vscode.window.showErrorMessage('NextCode: 网络连接失败');
        } else if (error.code === 'ETIMEDOUT') {
            this.settingsManager.log('请求超时');
        }
    }

    public refreshConfig(): void {
        this.settingsManager.refreshConfig();
        this.cache.clear(); // 清除缓存
    }

    public toggleEnabled(): void {
        this.isEnabled = !this.isEnabled;
        vscode.window.showInformationMessage(`NextCode 代码提示已${this.isEnabled ? '启用' : '禁用'}`);
    }

    public dispose(): void {
        if (this.debounceTimer) {
            clearTimeout(this.debounceTimer);
        }
        if (this.pendingRequest) {
            this.pendingRequest.abort();
            this.pendingRequest = null;
        }
        this.cache.clear();
    }
}