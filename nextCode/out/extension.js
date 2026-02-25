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
exports.settingsManager = exports.provider = exports.statusBarManager = void 0;
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const provider_1 = require("./provider");
const settings_1 = require("./settings");
const statusbar_1 = require("./statusbar");
function activate(context) {
    console.log('NextCode extension is now active!');
    // 初始化管理器
    exports.settingsManager = new settings_1.SettingsManager();
    exports.statusBarManager = new statusbar_1.StatusBarManager();
    exports.provider = new provider_1.NextCodeProvider();
    // 注册命令
    registerCommands(context);
    // 注册提供程序 - 使用更智能的触发条件
    const providerRegistration = vscode.languages.registerInlineCompletionItemProvider([
        { scheme: 'file', pattern: '**/*.{js,ts,jsx,tsx,py,java,c,cpp,go,rust,php,rb}' },
        { scheme: 'file', pattern: '**/*.{html,css,scss,less,json,xml,yaml,yml}' },
        { scheme: 'file', pattern: '**/*.{md,txt}' },
        { scheme: 'untitled' } // 未保存的文件
    ], exports.provider);
    // 订阅到上下文
    context.subscriptions.push(providerRegistration, exports.statusBarManager, exports.provider);
    // 初始化状态栏
    exports.statusBarManager.updateStatusBar();
    // 监听配置变化
    const configChangeDisposable = vscode.workspace.onDidChangeConfiguration((event) => {
        if (event.affectsConfiguration('nextCode')) {
            exports.provider.refreshConfig();
            exports.statusBarManager.updateStatusBar();
            // 检查是否是提供商变化，如果是则推荐默认模型
            if (event.affectsConfiguration('nextCode.apiProvider')) {
                const config = vscode.workspace.getConfiguration('nextCode');
                const provider = config.get('apiProvider', 'deepseek');
                const currentModel = config.get('model', '');
                const recommendedModel = settings_1.SettingsManager.getRecommendedModel(provider);
                // 如果当前模型为空或与推荐模型不匹配，提示用户
                if (!currentModel || currentModel === 'deepseek-chat') {
                    vscode.window.showInformationMessage(`NextCode: 推荐为 ${provider} 使用模型 "${recommendedModel}"`, '应用推荐', '保持当前').then(selection => {
                        if (selection === '应用推荐') {
                            config.update('model', recommendedModel, vscode.ConfigurationTarget.Global);
                        }
                    });
                }
            }
        }
    });
    context.subscriptions.push(configChangeDisposable);
    // 检查配置状态
    checkConfiguration();
    // 显示欢迎消息（仅首次）
    const hasShownWelcome = context.globalState.get('nextCode.hasShownWelcome', false);
    if (!hasShownWelcome) {
        vscode.window.showInformationMessage('🎉 NextCode 已激活！按 Tab 接受代码建议。', '打开设置', '不再显示').then(selection => {
            if (selection === '打开设置') {
                vscode.commands.executeCommand('nextCode.openSettings');
            }
            else if (selection === '不再显示') {
                context.globalState.update('nextCode.hasShownWelcome', true);
            }
        });
    }
}
function registerCommands(context) {
    // 打开设置
    const openSettingsCommand = vscode.commands.registerCommand('nextCode.openSettings', () => {
        vscode.commands.executeCommand('workbench.action.openSettings', '@ext:nextcode');
    });
    // 切换代码提示
    const toggleSuggestionsCommand = vscode.commands.registerCommand('nextCode.toggleSuggestions', async () => {
        const config = vscode.workspace.getConfiguration('nextCode');
        const current = config.get('enableInlineSuggestions', true);
        await config.update('enableInlineSuggestions', !current, vscode.ConfigurationTarget.Global);
        const message = `NextCode 代码提示已${!current ? '✅ 启用' : '❌ 禁用'}`;
        vscode.window.showInformationMessage(message);
    });
    // 显示使用量
    const showUsageCommand = vscode.commands.registerCommand('nextCode.showUsage', () => {
        exports.statusBarManager.showUsageDetails();
    });
    // 重置统计
    const resetStatsCommand = vscode.commands.registerCommand('nextCode.resetStats', () => {
        exports.statusBarManager.resetUsage();
    });
    // 手动触发补全（Ctrl+Shift+Space）
    const triggerCompletionCommand = vscode.commands.registerCommand('nextCode.triggerCompletion', () => {
        vscode.commands.executeCommand('editor.action.inlineSuggest.trigger');
    });
    // 接受当前建议
    const acceptCompletionCommand = vscode.commands.registerCommand('nextCode.acceptCompletion', () => {
        vscode.commands.executeCommand('editor.action.inlineSuggest.commit');
    });
    // 拒绝当前建议
    const rejectCompletionCommand = vscode.commands.registerCommand('nextCode.rejectCompletion', () => {
        vscode.commands.executeCommand('editor.action.inlineSuggest.hide');
    });
    // 打开设置页面（带侧边栏）
    const openSettingsSidebarCommand = vscode.commands.registerCommand('nextCode.openSettingsSidebar', () => {
        vscode.commands.executeCommand('workbench.action.openSettings', {
            query: '@ext:nextcode',
            openToSide: true
        });
    });
    context.subscriptions.push(openSettingsCommand, toggleSuggestionsCommand, showUsageCommand, resetStatsCommand, triggerCompletionCommand, acceptCompletionCommand, rejectCompletionCommand, openSettingsSidebarCommand);
}
function checkConfiguration() {
    const config = vscode.workspace.getConfiguration('nextCode');
    const apiKey = config.get('apiKey', '');
    const apiProvider = config.get('apiProvider', 'deepseek');
    if (!apiKey) {
        // 延迟显示配置提示，避免启动时弹出太多消息
        setTimeout(() => {
            vscode.window.showWarningMessage(`⚠️ NextCode: 请配置 ${apiProvider} 的 API 密钥`, '立即配置', '查看教程').then(selection => {
                if (selection === '立即配置') {
                    vscode.commands.executeCommand('nextCode.openSettings');
                }
                else if (selection === '查看教程') {
                    vscode.env.openExternal(vscode.Uri.parse('https://github.com/your-repo/nextcode#配置'));
                }
            });
        }, 3000);
    }
    else {
        exports.statusBarManager.updateStatusBar();
    }
}
function deactivate() {
    console.log('NextCode extension is now deactivated!');
    if (exports.provider) {
        exports.provider.dispose();
    }
    if (exports.statusBarManager) {
        exports.statusBarManager.dispose();
    }
}
//# sourceMappingURL=extension.js.map