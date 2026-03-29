/**
 * MediAssistant — Monolithic React App
 * Pixel-perfect mirror of templates/index.html + static/css/style.css + static/js/main.js
 *
 * Sections:
 *   1. Imports
 *   2. Utility helpers
 *   3. Sidebar component
 *   4. ChatArea component
 *   5. InputArea component
 *   6. App root (all state + API logic)
 */

import { useState, useEffect, useRef, useCallback } from 'react';
import ReactMarkdown from 'react-markdown';
import './index.css';

const BRAND_NAME = 'MediAssistant';
const API_BASE = '/api/v1';

const TRANSLATIONS = {
  en: {
    version: 'AI Assistant v3.0',
    newChat: 'New Chat',
    chatHistory: 'Chat History',
    loadingChats: 'Loading chats...',
    noChatHistory: 'No chat history yet',
    newConversation: 'New conversation',
    headerTitle: 'Medical AI Assistant',
    aiReady: 'AI Ready',
    clearConversation: 'Clear conversation',
    downloadChat: 'Download chat',
    settings: 'Settings',
    welcomeTitle: `Welcome to ${BRAND_NAME}`,
    welcomeSubtitle: 'Your AI-powered medical assistant is ready to help',
    quickQuestionsTitle: 'Quick Questions:',
    nearbyHospitalsButton: 'Find Nearby Hospitals',
    nearbyHospitalsTitle: 'Nearby Hospitals',
    nearbyHospitalsLoading: 'Searching nearby hospitals...',
    nearbyHospitalsError: 'Unable to fetch nearby hospitals right now.',
    nearbyHospitalsLocationError: 'Please allow location access to search nearby hospitals.',
    nearbyHospitalsEmpty: 'No nearby hospitals found. Try again later.',
    nearbyHospitalDistance: 'Distance',
    nearbyHospitalAddress: 'Address',
    nearbyHospitalPhone: 'Phone',
    nearbyHospitalNavigation: 'Navigate',
    quickQuestions: [
      { icon: 'fa-thermometer', label: 'Fever Symptoms', q: 'What are the symptoms of fever?' },
      { icon: 'fa-head-side-virus', label: 'Headache Treatment', q: 'How to treat a headache?' },
      { icon: 'fa-heart-pulse', label: 'High Blood Pressure', q: 'What causes high blood pressure?' },
      { icon: 'fa-notes-medical', label: 'Diabetes Management', q: 'Tell me about diabetes management' },
      { icon: 'fa-virus-covid', label: 'COVID Prevention', q: 'COVID-19 prevention tips' },
      { icon: 'fa-pills', label: 'Cold Remedies', q: 'Common cold remedies' },
    ],
    features: [
      { icon: 'fa-brain', label: 'AI-Powered' },
      { icon: 'fa-database', label: 'Medical Database' },
      { icon: 'fa-shield-alt', label: 'Reliable Info' },
    ],
    thinking: `${BRAND_NAME} is thinking`,
    copy: 'Copy',
    attachFile: 'Attach file',
    voiceInput: 'Voice input',
    askPlaceholder: 'Ask your medical question...',
    sendMessage: 'Send message',
    disclaimer: 'AI can make mistakes. Always consult healthcare professionals for medical advice.',
    switchToChinese: '切换到中文',
    switchToEnglish: 'Switch to English',
    languageButtonLabel: '中',
    themeToggle: 'Toggle theme',
    deleteChatTitle: 'Delete chat',
    clearChatTitle: 'Clear conversation',
    confirmAction: 'Delete',
    confirmClear: 'Clear',
    cancelAction: 'Cancel',
    deleteConfirm: 'Are you sure you want to delete this chat?',
    clearConfirm: 'Are you sure you want to clear this conversation?',
    chatLoaded: 'Chat loaded successfully',
    failedLoadChat: 'Failed to load chat',
    chatDeleted: 'Chat deleted successfully',
    failedDeleteChat: 'Failed to delete chat',
    newChatCreated: 'New chat created',
    failedCreateChat: 'Failed to create new chat',
    conversationCleared: 'Conversation cleared',
    failedClearConversation: 'Failed to clear conversation',
    noMessagesToDownload: 'No messages to download',
    chatDownloaded: 'Chat downloaded successfully',
    responseReceived: 'Response received',
    errorOccurred: 'Error occurred',
    connectionError: 'Connection error',
    assistantError: 'Sorry, I encountered an error. Please try again.',
    assistantConnectionError: 'Connection error. Please check your internet and try again.',
    exportTitle: `${BRAND_NAME} Chat Export`,
    you: 'You',
    assistant: BRAND_NAME,
    source: 'Source',
    browserTitle: `${BRAND_NAME} - AI Medical Assistant`,
    justNow: 'Just now',
    minuteAgo: (count) => `${count}m ago`,
    hourAgo: (count) => `${count}h ago`,
    dayAgo: (count) => `${count}d ago`,
  },
  zh: {
    version: 'AI 助手 v3.0',
    newChat: '新建聊天',
    chatHistory: '聊天记录',
    loadingChats: '正在加载聊天...',
    noChatHistory: '暂无聊天记录',
    newConversation: '新对话',
    headerTitle: '医疗 AI 助手',
    aiReady: 'AI 已就绪',
    clearConversation: '清空对话',
    downloadChat: '下载聊天',
    settings: '设置',
    welcomeTitle: `欢迎使用 ${BRAND_NAME}`,
    welcomeSubtitle: '你的 AI 医疗助手已准备好为你提供帮助',
    quickQuestionsTitle: '快捷提问：',
    nearbyHospitalsButton: '查询附近医院',
    nearbyHospitalsTitle: '附近医院',
    nearbyHospitalsLoading: '正在查询附近医院...',
    nearbyHospitalsError: '暂时无法查询附近医院，请稍后再试。',
    nearbyHospitalsLocationError: '请允许定位权限后再查询附近医院。',
    nearbyHospitalsEmpty: '附近暂无医院结果，请稍后重试。',
    nearbyHospitalDistance: '距离',
    nearbyHospitalAddress: '地址',
    nearbyHospitalPhone: '电话',
    nearbyHospitalNavigation: '导航',
    quickQuestions: [
      { icon: 'fa-thermometer', label: '发烧症状', q: '发烧通常有哪些症状？' },
      { icon: 'fa-head-side-virus', label: '头痛处理', q: '头痛该如何缓解？' },
      { icon: 'fa-heart-pulse', label: '高血压', q: '高血压通常由什么引起？' },
      { icon: 'fa-notes-medical', label: '糖尿病管理', q: '请介绍一下糖尿病管理方法。' },
      { icon: 'fa-virus-covid', label: '新冠预防', q: '有哪些新冠预防建议？' },
      { icon: 'fa-pills', label: '感冒缓解', q: '常见感冒有哪些缓解方法？' },
    ],
    features: [
      { icon: 'fa-brain', label: 'AI 驱动' },
      { icon: 'fa-database', label: '医疗知识库' },
      { icon: 'fa-shield-alt', label: '可靠信息' },
    ],
    thinking: `${BRAND_NAME} 正在思考`,
    copy: '复制',
    attachFile: '添加附件',
    voiceInput: '语音输入',
    askPlaceholder: '请输入你的医疗问题...',
    sendMessage: '发送消息',
    disclaimer: 'AI 可能出错。医疗建议请始终咨询专业医护人员。',
    switchToChinese: '切换到中文',
    switchToEnglish: 'Switch to English',
    languageButtonLabel: 'EN',
    themeToggle: '切换主题',
    deleteChatTitle: '删除聊天',
    clearChatTitle: '清空对话',
    confirmAction: '删除',
    confirmClear: '清空',
    cancelAction: '取消',
    deleteConfirm: '确定要删除这条聊天吗？',
    clearConfirm: '确定要清空当前对话吗？',
    chatLoaded: '聊天加载成功',
    failedLoadChat: '聊天加载失败',
    chatDeleted: '聊天删除成功',
    failedDeleteChat: '聊天删除失败',
    newChatCreated: '已创建新聊天',
    failedCreateChat: '创建新聊天失败',
    conversationCleared: '对话已清空',
    failedClearConversation: '清空对话失败',
    noMessagesToDownload: '没有可下载的消息',
    chatDownloaded: '聊天下载成功',
    responseReceived: '已收到回复',
    errorOccurred: '发生错误',
    connectionError: '连接错误',
    assistantError: '抱歉，出现了一点问题，请稍后重试。',
    assistantConnectionError: '连接异常，请检查网络后重试。',
    exportTitle: `${BRAND_NAME} 聊天导出`,
    you: '你',
    assistant: BRAND_NAME,
    source: '来源',
    browserTitle: `${BRAND_NAME} - 医疗 AI 助手`,
    justNow: '刚刚',
    minuteAgo: (count) => `${count} 分钟前`,
    hourAgo: (count) => `${count} 小时前`,
    dayAgo: (count) => `${count} 天前`,
  },
};

function formatTimeAgo(timestamp, t) {
  const now = new Date();
  const past = new Date(timestamp);
  const diffMs = now - past;
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) return t.justNow;
  if (diffMins < 60) return t.minuteAgo(diffMins);
  if (diffHours < 24) return t.hourAgo(diffHours);
  if (diffDays < 7) return t.dayAgo(diffDays);
  return past.toLocaleDateString();
}

function buildDownloadText(chatHistory, t) {
  let content = `${t.exportTitle}\n`;
  content += '='.repeat(50) + '\n\n';
  chatHistory.forEach((msg) => {
    content += `[${msg.timestamp}] ${msg.type === 'user' ? t.you : t.assistant}:\n`;
    content += msg.content + '\n';
    if (msg.source) content += `${t.source}: ${msg.source}\n`;
    content += '\n';
  });
  return content;
}

function Sidebar({
  sidebarOpen,
  sessions,
  currentSessionId,
  onNewChat,
  onLoadSession,
  onDeleteSession,
  onToggleTheme,
  onToggleLanguage,
  onNearbyHospitalSearch,
  theme,
  language,
  t,
}) {
  return (
    <aside className={`sidebar glass-effect${sidebarOpen ? '' : ' collapsed'}`}>
      <div className="sidebar-content">
        <div className="sidebar-header">
          <div className="logo-wrapper">
            <div className="logo-animated">
              <div className="logo-pulse" />
              <i className="fas fa-heartbeat" />
            </div>
            <div className="logo-text">
              <h1>{BRAND_NAME}</h1>
              <span className="version">{t.version}</span>
            </div>
          </div>
          <button className="new-chat-btn" onClick={onNewChat}>
            <i className="fas fa-plus" />
            <span>{t.newChat}</span>
          </button>
        </div>

        <div className="chat-history-section">
          <div className="section-header">
            <span>{t.chatHistory}</span>
            <div className="section-line" />
          </div>
          <div className="chat-list">
            {sessions === null ? (
              <div style={{ textAlign: 'center', padding: '20px', color: 'var(--text-tertiary)', fontSize: '13px' }}>
                <div className="loading-spinner" style={{ margin: '0 auto 10px' }} />
                {t.loadingChats}
              </div>
            ) : sessions.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '20px', color: 'var(--text-tertiary)', fontSize: '13px' }}>
                {t.noChatHistory}
              </div>
            ) : (
              sessions.map((session) => (
                <div
                  key={session.session_id}
                  className={`chat-item${currentSessionId === session.session_id ? ' active' : ''}`}
                  onClick={() => onLoadSession(session.session_id)}
                >
                  <i className="fas fa-message" />
                  <div className="chat-item-content">
                    <div className="chat-item-title">{session.preview || t.newConversation}</div>
                    <div className="chat-item-time">{formatTimeAgo(session.last_active, t)}</div>
                  </div>
                  <button
                    className="chat-item-delete"
                    onClick={(e) => { e.stopPropagation(); onDeleteSession(session.session_id); }}
                  >
                    <i className="fas fa-trash" />
                  </button>
                </div>
              ))
            )}
          </div>
        </div>

        <div className="sidebar-footer">
          <button
            className="theme-btn glass-effect"
            onClick={onToggleLanguage}
            aria-label={language === 'en' ? t.switchToChinese : t.switchToEnglish}
            title={language === 'en' ? t.switchToChinese : t.switchToEnglish}
            style={{ marginBottom: '10px' }}
          >
            {t.languageButtonLabel}
          </button>
          <button
            className="theme-btn glass-effect"
            onClick={onNearbyHospitalSearch}
            aria-label={t.nearbyHospitalsButton}
            title={t.nearbyHospitalsButton}
            style={{ marginBottom: '10px' }}
          >
            <i className="fas fa-hospital" />
          </button>
          <button className="theme-btn glass-effect" onClick={onToggleTheme} aria-label={t.themeToggle} title={t.themeToggle}>
            <i className={`fas ${theme === 'dark' ? 'fa-sun' : 'fa-moon'}`} />
          </button>
        </div>
      </div>
    </aside>
  );
}

function ChatArea({
  messages,
  isTyping,
  showWelcome,
  onQuickQuestion,
  onNearbyHospitalSearch,
  hospitalSearch,
  chatAreaRef,
  t,
}) {
  return (
    <div className="chat-area" ref={chatAreaRef}>
      <div className={`welcome-screen${showWelcome ? '' : ' hidden'}`}>
        <div className="welcome-content">
          <div className="logo-3d">
            <i className="fas fa-stethoscope" />
          </div>
          <h1 className="welcome-title">{t.welcomeTitle}</h1>
          <p className="welcome-subtitle">{t.welcomeSubtitle}</p>

          <div className="quick-actions">
            <h3>{t.quickQuestionsTitle}</h3>
            <div className="quick-buttons">
              {t.quickQuestions.map(({ icon, label, q }) => (
                <button key={q} className="quick-btn glass-effect" onClick={() => onQuickQuestion(q)}>
                  <i className={`fas ${icon}`} />
                  <span>{label}</span>
                </button>
              ))}
            </div>
          </div>

          {(hospitalSearch.hasSearched || hospitalSearch.isLoading || hospitalSearch.error || hospitalSearch.results.length > 0) && (
            <div className="nearby-hospital-panel glass-effect">
              <h3>{t.nearbyHospitalsTitle}</h3>
              {hospitalSearch.isLoading && (
                <p className="nearby-hospital-status">{t.nearbyHospitalsLoading}</p>
              )}
              {!hospitalSearch.isLoading && hospitalSearch.error && (
                <p className="nearby-hospital-status error">{hospitalSearch.error}</p>
              )}
              {!hospitalSearch.isLoading && !hospitalSearch.error && hospitalSearch.results.length === 0 && (
                <p className="nearby-hospital-status">{t.nearbyHospitalsEmpty}</p>
              )}
              <div className="nearby-hospital-list">
                {hospitalSearch.results.map((hospital) => (
                  <article key={hospital.id} className="nearby-hospital-card">
                    <div className="nearby-hospital-card-header">
                      <h4>{hospital.name}</h4>
                      {hospital.is_tertiary_a && hospital.level && (
                        <span className="nearby-hospital-level">{hospital.level}</span>
                      )}
                    </div>
                    <p>{t.nearbyHospitalDistance}: {hospital.distance_text}</p>
                    <p>{t.nearbyHospitalAddress}: {hospital.address}</p>
                    {hospital.phone && <p>{t.nearbyHospitalPhone}: {hospital.phone}</p>}
                    {hospital.navigation_url && (
                      <a
                        className="nearby-hospital-link"
                        href={hospital.navigation_url}
                        target="_blank"
                        rel="noreferrer"
                      >
                        {t.nearbyHospitalNavigation}
                      </a>
                    )}
                  </article>
                ))}
              </div>
            </div>
          )}

          <div className="features">
            {t.features.map(({ icon, label }) => (
              <div key={label} className="feature-card glass-effect">
                <i className={`fas ${icon}`} />
                <span>{label}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="messages-container">
        {messages.map((msg, idx) => (
          <MessageBubble key={idx} msg={msg} t={t} />
        ))}
      </div>

      <div className={`typing-indicator${isTyping ? ' active' : ''}`}>
        <div className="typing-bubble glass-effect">
          <div className="typing-content">
            <span className="typing-text">{t.thinking}</span>
            <div className="typing-dots">
              <span className="dot" />
              <span className="dot" />
              <span className="dot" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function MessageBubble({ msg, t }) {
  const copyText = useCallback(() => {
    navigator.clipboard.writeText(msg.content).catch(() => { });
  }, [msg.content]);

  if (msg.type === 'user') {
    return (
      <div className="message user-message">
        <div className="message-wrapper">
          <div className="message-avatar"><i className="fas fa-user" /></div>
          <div className="message-content">
            <div className="message-text">
              {msg.content}
              <span className="message-time">{msg.timestamp}</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="message bot-message">
      <div className="message-wrapper">
        <div className="message-avatar"><i className="fas fa-robot" /></div>
        <div className="message-content">
          <div className="message-text">
            <ReactMarkdown>{msg.content}</ReactMarkdown>
          </div>
          <span className="message-time">{msg.timestamp}</span>
          <div className="message-footer">
            {msg.source && (
              <span className="message-source">
                <i className="fas fa-database" />
                {msg.source}
              </span>
            )}
            <div className="message-actions">
              <button className="message-action" title={t.copy} onClick={copyText}>
                <i className="fas fa-copy" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function InputArea({ inputValue, setInputValue, onSend, isTyping, inputRef, t }) {
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSend();
    }
  };

  const handleInput = (e) => {
    setInputValue(e.target.value);
    e.target.style.height = 'auto';
    e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px';
  };

  return (
    <div className="input-area">
      <div className="input-wrapper">
        <div className="input-container glass-effect">
          <button className="input-btn" title={t.attachFile}>
            <i className="fas fa-paperclip" />
          </button>
          <textarea
            ref={inputRef}
            className="message-input"
            placeholder={t.askPlaceholder}
            rows={1}
            value={inputValue}
            onChange={handleInput}
            onKeyDown={handleKeyDown}
          />
          <button className="input-btn" title={t.voiceInput}>
            <i className="fas fa-microphone" />
          </button>
          <button
            className="send-btn"
            title={t.sendMessage}
            aria-label={t.sendMessage}
            onClick={onSend}
            disabled={!inputValue.trim() || isTyping}
          >
            <i className="fas fa-paper-plane" />
          </button>
        </div>
        <div className="input-info">
          <i className="fas fa-info-circle" />
          <span>{t.disclaimer}</span>
        </div>
      </div>
    </div>
  );
}

function ConfirmModal({ dialog, onCancel }) {
  if (!dialog.isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onCancel}>
      <div
        className="confirm-modal glass-effect"
        role="dialog"
        aria-modal="true"
        aria-labelledby="confirm-modal-title"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="confirm-modal-header">
          <div className="confirm-modal-icon">
            <i className="fas fa-triangle-exclamation" />
          </div>
          <h3 id="confirm-modal-title">{dialog.title}</h3>
        </div>
        <p className="confirm-modal-message">{dialog.message}</p>
        <div className="confirm-modal-actions">
          <button className="confirm-modal-btn secondary" onClick={onCancel}>
            {dialog.cancelLabel}
          </button>
          <button className="confirm-modal-btn danger" onClick={dialog.onConfirm}>
            {dialog.confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
}
function useIsMobile(breakpoint = 768) {
  const [isMobile, setIsMobile] = useState(() => window.innerWidth <= breakpoint);

  useEffect(() => {
    const handler = () => setIsMobile(window.innerWidth <= breakpoint);
    window.addEventListener('resize', handler);
    return () => window.removeEventListener('resize', handler);
  }, [breakpoint]);

  return isMobile;
}

export default function App() {
  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'light');
  const [language, setLanguage] = useState('zh');
  const isMobile = useIsMobile();
  const [sidebarOpen, setSidebarOpen] = useState(() => {
    if (window.innerWidth <= 768) return false;
    return localStorage.getItem('sidebarOpen') !== 'false';
  });
  const [sessions, setSessions] = useState(null);
  const [currentSessionId, setCurrentSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [chatHistory, setChatHistory] = useState([]);
  const [showWelcome, setShowWelcome] = useState(true);
  const [isTyping, setIsTyping] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [toast, setToast] = useState({ show: false, message: '', type: 'success' });
  const [hospitalSearch, setHospitalSearch] = useState({
    isLoading: false,
    error: '',
    results: [],
    hasSearched: false,
  });
  const [confirmDialog, setConfirmDialog] = useState({
    isOpen: false,
    title: '',
    message: '',
    confirmLabel: '',
    cancelLabel: '',
    onConfirm: null,
  });

  const t = TRANSLATIONS[language];
  const chatAreaRef = useRef(null);
  const inputRef = useRef(null);
  const toastTimerRef = useRef(null);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  useEffect(() => {
    document.title = t.browserTitle;
  }, [t]);

  const toggleTheme = () => setTheme((prevTheme) => (prevTheme === 'light' ? 'dark' : 'light'));
  const toggleLanguage = () => setLanguage((prevLanguage) => (prevLanguage === 'en' ? 'zh' : 'en'));

  const toggleSidebar = () => {
    setSidebarOpen((prevOpen) => {
      if (!isMobile) localStorage.setItem('sidebarOpen', !prevOpen);
      return !prevOpen;
    });
  };

  const closeSidebar = () => setSidebarOpen(false);

  const closeConfirmDialog = useCallback(() => {
    setConfirmDialog({
      isOpen: false,
      title: '',
      message: '',
      confirmLabel: '',
      cancelLabel: '',
      onConfirm: null,
    });
  }, []);

  const openConfirmDialog = useCallback((config) => {
    setConfirmDialog({
      isOpen: true,
      title: config.title,
      message: config.message,
      confirmLabel: config.confirmLabel,
      cancelLabel: config.cancelLabel,
      onConfirm: async () => {
        await config.onConfirm();
        closeConfirmDialog();
      },
    });
  }, [closeConfirmDialog]);

  const showToast = useCallback((message, type = 'success') => {
    if (toastTimerRef.current) clearTimeout(toastTimerRef.current);
    setToast({ show: true, message, type });
    toastTimerRef.current = setTimeout(() => setToast((prevToast) => ({ ...prevToast, show: false })), 3000);
  }, []);

  const scrollToBottom = useCallback(() => {
    if (chatAreaRef.current) {
      chatAreaRef.current.scrollTo({ top: chatAreaRef.current.scrollHeight, behavior: 'smooth' });
    }
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping, scrollToBottom]);

  const loadSessions = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/sessions`);
      const data = await res.json();
      if (data.success && data.sessions) setSessions(data.sessions);
    } catch {
      setSessions([]);
    }
  }, []);

  useEffect(() => {
    loadSessions();
    (async () => {
      try {
        const res = await fetch(`${API_BASE}/history`);
        const data = await res.json();
        if (data.success && data.messages && data.messages.length > 0) {
          const msgs = data.messages.map((message) => ({
            type: message.role === 'user' ? 'user' : 'assistant',
            content: message.content,
            timestamp: message.timestamp || '',
            source: message.source || null,
          }));
          setMessages(msgs);
          setChatHistory(msgs.map((message) => ({ ...message })));
          setShowWelcome(false);
        }
      } catch {
      }
    })();
  }, [loadSessions]);

  const loadSession = useCallback(async (sessionId) => {
    try {
      const res = await fetch(`${API_BASE}/session/${sessionId}`);
      const data = await res.json();
      if (data.success) {
        setCurrentSessionId(sessionId);
        const msgs = data.messages.map((message) => ({
          type: message.role === 'user' ? 'user' : 'assistant',
          content: message.content,
          timestamp: message.timestamp || '',
          source: message.source || null,
        }));
        setMessages(msgs);
        setChatHistory(msgs.map((message) => ({ ...message })));
        setShowWelcome(false);
        showToast(t.chatLoaded, 'success');
      }
    } catch {
      showToast(t.failedLoadChat, 'error');
    }
  }, [showToast, t]);

  const createNewChat = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/new-chat`, { method: 'POST' });
      if (res.ok) {
        setMessages([]);
        setChatHistory([]);
        setCurrentSessionId(null);
        setShowWelcome(true);
        await loadSessions();
        showToast(t.newChatCreated, 'success');
      }
    } catch {
      showToast(t.failedCreateChat, 'error');
    }
  }, [loadSessions, showToast, t]);

  const deleteSession = useCallback((sessionId) => {
    openConfirmDialog({
      title: t.deleteChatTitle,
      message: t.deleteConfirm,
      confirmLabel: t.confirmAction,
      cancelLabel: t.cancelAction,
      onConfirm: async () => {
        try {
          const res = await fetch(`${API_BASE}/session/${sessionId}`, { method: 'DELETE' });
          if (res.ok) {
            await loadSessions();
            if (currentSessionId === sessionId) createNewChat();
            showToast(t.chatDeleted, 'success');
          }
        } catch {
          showToast(t.failedDeleteChat, 'error');
        }
      },
    });
  }, [createNewChat, currentSessionId, loadSessions, openConfirmDialog, showToast, t]);

  const clearChat = useCallback(() => {
    openConfirmDialog({
      title: t.clearChatTitle,
      message: t.clearConfirm,
      confirmLabel: t.confirmClear,
      cancelLabel: t.cancelAction,
      onConfirm: async () => {
        try {
          const res = await fetch(`${API_BASE}/clear`, { method: 'POST' });
          if (res.ok) {
            setMessages([]);
            setChatHistory([]);
            setShowWelcome(true);
            showToast(t.conversationCleared, 'success');
          }
        } catch {
          showToast(t.failedClearConversation, 'error');
        }
      },
    });
  }, [openConfirmDialog, showToast, t]);

  const downloadChat = useCallback(() => {
    if (chatHistory.length === 0) {
      showToast(t.noMessagesToDownload, 'error');
      return;
    }

    const content = buildDownloadText(chatHistory, t);
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `mediassistant-chat-${Date.now()}.txt`;
    link.click();
    URL.revokeObjectURL(url);
    showToast(t.chatDownloaded, 'success');
  }, [chatHistory, showToast, t]);

  const searchNearbyHospitals = useCallback(() => {
    const geolocation = navigator.geolocation;
    if (!geolocation) {
      setHospitalSearch({ isLoading: false, error: t.nearbyHospitalsLocationError, results: [], hasSearched: true });
      return;
    }

    setHospitalSearch({ isLoading: true, error: '', results: [], hasSearched: true });

    geolocation.getCurrentPosition(
      async ({ coords }) => {
        try {
          const response = await fetch(`${API_BASE}/hospitals/nearby`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              latitude: coords.latitude,
              longitude: coords.longitude,
              radius_meters: 5000,
              limit: 10,
            }),
          });
          const data = await response.json();

          if (!response.ok || !data.success) {
            throw new Error('hospital_search_failed');
          }

          setHospitalSearch({
            isLoading: false,
            error: '',
            results: data.hospitals || [],
            hasSearched: true,
          });
        } catch {
          setHospitalSearch({ isLoading: false, error: t.nearbyHospitalsError, results: [], hasSearched: true });
        }
      },
      () => {
        setHospitalSearch({ isLoading: false, error: t.nearbyHospitalsLocationError, results: [], hasSearched: true });
      },
    );
  }, [t]);

  const sendMessage = useCallback(async (overrideText) => {
    const message = (overrideText ?? inputValue).trim();
    if (!message || isTyping) return;

    setShowWelcome(false);
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const userMessage = { type: 'user', content: message, timestamp: time, source: null };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setChatHistory((prevHistory) => [...prevHistory, userMessage]);
    setInputValue('');
    if (inputRef.current) inputRef.current.style.height = 'auto';
    setIsTyping(true);

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, language }),
      });
      const data = await res.json();

      if (data.success) {
        const assistantMessage = {
          type: 'assistant',
          content: data.response,
          timestamp: data.timestamp || time,
          source: data.source || null,
        };
        setMessages((prevMessages) => [...prevMessages, assistantMessage]);
        setChatHistory((prevHistory) => [...prevHistory, assistantMessage]);
        showToast(t.responseReceived, 'success');
        await loadSessions();
      } else {
        const errorMessage = {
          type: 'assistant',
          content: t.assistantError,
          timestamp: time,
          source: null,
        };
        setMessages((prevMessages) => [...prevMessages, errorMessage]);
        showToast(t.errorOccurred, 'error');
      }
    } catch {
      const errorMessage = {
        type: 'assistant',
        content: t.assistantConnectionError,
        timestamp: time,
        source: null,
      };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
      showToast(t.connectionError, 'error');
    } finally {
      setIsTyping(false);
    }
  }, [inputValue, isTyping, language, loadSessions, showToast, t]);

  const handleQuickQuestion = useCallback((question) => {
    setTimeout(() => sendMessage(question), 200);
  }, [sendMessage]);

  const toastColors = {
    success: 'linear-gradient(135deg, #10b981, #059669)',
    error: 'linear-gradient(135deg, #ef4444, #dc2626)',
    info: 'linear-gradient(135deg, #3b82f6, #2563eb)',
  };

  const toastIcons = {
    success: 'fa-check-circle',
    error: 'fa-exclamation-circle',
    info: 'fa-info-circle',
  };

  return (
    <>
      <div className="animated-background">
        <div className="gradient-overlay" />
        <div className="floating-circles">
          <div className="circle circle-1" />
          <div className="circle circle-2" />
          <div className="circle circle-3" />
        </div>
      </div>

      <div className="app-container">
        <button className="sidebar-toggle-btn" onClick={toggleSidebar}>
          <i className="fas fa-bars" />
        </button>

        {isMobile && sidebarOpen && (
          <div className="sidebar-backdrop" onClick={closeSidebar} />
        )}

        <Sidebar
          sidebarOpen={sidebarOpen}
          sessions={sessions}
          currentSessionId={currentSessionId}
          onNewChat={createNewChat}
          onLoadSession={loadSession}
          onDeleteSession={deleteSession}
          onToggleTheme={toggleTheme}
          onToggleLanguage={toggleLanguage}
          onNearbyHospitalSearch={searchNearbyHospitals}
          theme={theme}
          language={language}
          t={t}
        />

        <main className={`main-content${sidebarOpen ? ' sidebar-open' : ''}`}>
          <header className="app-header glass-header">
            <div className="header-content">
              <h2 className="gradient-text">{t.headerTitle}</h2>
              <div className="status-indicator">
                <div className="status-ring">
                  <span className="ring-pulse" />
                </div>
                <span>{t.aiReady}</span>
              </div>
            </div>
            <div className="header-actions">
              <button className="action-btn" title={t.clearConversation} onClick={clearChat}>
                <i className="fas fa-trash" />
              </button>
              <button className="action-btn" title={t.downloadChat} onClick={downloadChat}>
                <i className="fas fa-download" />
              </button>
              <button className="action-btn" title={t.settings}>
                <i className="fas fa-cog" />
              </button>
            </div>
          </header>

          <ChatArea
            messages={messages}
            isTyping={isTyping}
            showWelcome={showWelcome}
            onQuickQuestion={handleQuickQuestion}
            onNearbyHospitalSearch={searchNearbyHospitals}
            hospitalSearch={hospitalSearch}
            chatAreaRef={chatAreaRef}
            t={t}
          />

          <InputArea
            inputValue={inputValue}
            setInputValue={setInputValue}
            onSend={() => sendMessage()}
            isTyping={isTyping}
            inputRef={inputRef}
            t={t}
          />
        </main>
      </div>

      <ConfirmModal dialog={confirmDialog} onCancel={closeConfirmDialog} />

      <div className={`toast${toast.show ? ' show' : ''}`} style={{ background: toastColors[toast.type] }}>
        <i className={`fas ${toastIcons[toast.type]}`} />
        <span>{toast.message}</span>
      </div>
    </>
  );
}





