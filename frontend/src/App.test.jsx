import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import App from './App';

describe('App Integration', () => {
    const mockFetch = vi.fn();
    global.fetch = mockFetch;

    beforeEach(() => {
        mockFetch.mockClear();
        mockFetch.mockResolvedValue({
            json: () => Promise.resolve({ success: true, messages: [], sessions: [] }),
            ok: true
        });
    });

    afterEach(() => {
        vi.restoreAllMocks();
    });

    it('renders app structure', async () => {
        render(<App />);
        expect(screen.getByText('Medical AI Assistant')).toBeInTheDocument();
        expect(screen.getByText('MediAssistant')).toBeInTheDocument();
        expect(screen.getByPlaceholderText('Ask your medical question...')).toBeInTheDocument();
    });

    it('toggles interface language between English and Chinese', async () => {
        render(<App />);

        const languageBtn = screen.getByRole('button', { name: /中文|切换/i });
        fireEvent.click(languageBtn);

        expect(screen.getByText('医疗 AI 助手')).toBeInTheDocument();
        expect(screen.getByText('MediAssistant')).toBeInTheDocument();
        expect(screen.getByText('新建聊天')).toBeInTheDocument();
        expect(screen.getByPlaceholderText('请输入你的医疗问题...')).toBeInTheDocument();

        fireEvent.click(screen.getByRole('button', { name: 'Switch to English' }));
        expect(screen.getByText('Medical AI Assistant')).toBeInTheDocument();
        expect(screen.getByText('New Chat')).toBeInTheDocument();
    });

    it('shows in-page delete confirmation modal before deleting chat', async () => {
        const mockSessions = [{ session_id: '1', preview: 'Flu symptoms', last_active: '2023-01-01' }];
        mockFetch.mockImplementation((url, options) => {
            if (url === '/api/v1/sessions') {
                return Promise.resolve({
                    json: () => Promise.resolve({ success: true, sessions: mockSessions }),
                    ok: true,
                });
            }
            if (url === '/api/v1/session/1' && options?.method === 'DELETE') {
                return Promise.resolve({ ok: true, json: () => Promise.resolve({ success: true }) });
            }
            return Promise.resolve({ json: () => Promise.resolve({ success: true, sessions: [] }), ok: true });
        });

        const { container } = render(<App />);

        await waitFor(() => {
            expect(screen.getByText('Flu symptoms')).toBeInTheDocument();
        });

        fireEvent.click(container.querySelector('.chat-item-delete'));

        expect(screen.getByRole('dialog')).toBeInTheDocument();
        expect(screen.getByText('Delete chat')).toBeInTheDocument();
        expect(mockFetch).not.toHaveBeenCalledWith('/api/v1/session/1', expect.objectContaining({ method: 'DELETE' }));

        fireEvent.click(screen.getByRole('button', { name: 'Delete' }));

        await waitFor(() => {
            expect(mockFetch).toHaveBeenCalledWith('/api/v1/session/1', expect.objectContaining({ method: 'DELETE' }));
        });
    });

    it('shows in-page clear confirmation modal before clearing conversation', async () => {
        mockFetch.mockImplementation((url, options) => {
            if (url === '/api/v1/clear' && options?.method === 'POST') {
                return Promise.resolve({ ok: true, json: () => Promise.resolve({ success: true }) });
            }
            return Promise.resolve({ json: () => Promise.resolve({ success: true, sessions: [] }), ok: true });
        });

        render(<App />);

        fireEvent.click(screen.getByTitle('Clear conversation'));

        expect(screen.getByRole('dialog')).toBeInTheDocument();
        expect(screen.getByText('Clear conversation')).toBeInTheDocument();
        expect(mockFetch).not.toHaveBeenCalledWith('/api/v1/clear', expect.objectContaining({ method: 'POST' }));

        fireEvent.click(screen.getByRole('button', { name: 'Cancel' }));
        expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
        expect(mockFetch).not.toHaveBeenCalledWith('/api/v1/clear', expect.objectContaining({ method: 'POST' }));
    });

    it('loads sessions on mount', async () => {
        const mockSessions = [{ session_id: '1', preview: 'Flu symptoms', last_active: '2023' }];
        mockFetch.mockImplementation((url) => {
            if (url === '/api/v1/sessions') {
                return Promise.resolve({
                    json: () => Promise.resolve({ success: true, sessions: mockSessions }),
                    ok: true
                });
            }
            return Promise.resolve({ json: () => Promise.resolve({ success: true }), ok: true });
        });

        render(<App />);

        await waitFor(() => {
            expect(screen.getByText('Flu symptoms')).toBeInTheDocument();
        });
    });

    it('sends a message and displays response', async () => {
        mockFetch.mockImplementation((url) => {
            if (url === '/api/v1/chat') {
                return Promise.resolve({
                    json: () => Promise.resolve({
                        success: true,
                        response: 'I can help with that.',
                        source: 'test-source',
                        timestamp: 'now'
                    }),
                    ok: true
                });
            }
            return Promise.resolve({ json: () => Promise.resolve({ success: true, sessions: [] }), ok: true });
        });

        render(<App />);

        const input = screen.getByPlaceholderText('Ask your medical question...');
        fireEvent.change(input, { target: { value: 'Headache' } });

        const sendBtn = screen.getByRole('button', { name: /Send message/i });
        fireEvent.click(sendBtn);

        expect(screen.getByText('Headache')).toBeInTheDocument();

        await waitFor(() => {
            expect(screen.getByText('I can help with that.')).toBeInTheDocument();
        });
    });

    it('sends current interface language with chat request', async () => {
        mockFetch.mockImplementation((url) => {
            if (url === '/api/v1/chat') {
                return Promise.resolve({
                    json: () => Promise.resolve({
                        success: true,
                        response: '好的，我来帮助你。',
                        source: 'test-source',
                        timestamp: 'now'
                    }),
                    ok: true
                });
            }
            return Promise.resolve({ json: () => Promise.resolve({ success: true, sessions: [] }), ok: true });
        });

        render(<App />);

        fireEvent.click(screen.getByRole('button', { name: /中文|切换/i }));

        const input = screen.getByPlaceholderText('请输入你的医疗问题...');
        fireEvent.change(input, { target: { value: '发烧怎么办' } });
        fireEvent.click(screen.getByRole('button', { name: '发送消息' }));

        await waitFor(() => {
            expect(mockFetch).toHaveBeenCalledWith('/api/v1/chat', expect.objectContaining({
                method: 'POST',
                body: JSON.stringify({ message: '发烧怎么办', language: 'zh' }),
            }));
        });
    });

    it('creates new chat', async () => {
        mockFetch.mockImplementation((url) => {
            if (url === '/api/v1/new-chat') {
                return Promise.resolve({
                    json: () => Promise.resolve({ success: true, session_id: 'new-session' }),
                    ok: true
                });
            }
            return Promise.resolve({ json: () => Promise.resolve({ success: true, sessions: [] }), ok: true });
        });

        render(<App />);

        const newChatBtn = screen.getByText('New Chat');
        fireEvent.click(newChatBtn);

        await waitFor(() => {
            expect(mockFetch).toHaveBeenCalledWith('/api/v1/new-chat', expect.any(Object));
        });
    });

    it('requests geolocation and renders nearby hospitals', async () => {
        const geolocationMock = vi.fn((success) => {
            success({
                coords: {
                    latitude: 31.2304,
                    longitude: 121.4737,
                },
            });
        });

        Object.defineProperty(global.navigator, 'geolocation', {
            configurable: true,
            value: {
                getCurrentPosition: geolocationMock,
            },
        });

        mockFetch.mockImplementation((url, options) => {
            if (url === '/api/v1/hospitals/nearby') {
                return Promise.resolve({
                    ok: true,
                    json: () => Promise.resolve({
                        success: true,
                        hospitals: [
                            {
                                id: 'hospital_001',
                                name: '复旦大学附属中山医院',
                                level: '三甲医院',
                                is_tertiary_a: true,
                                distance_meters: 1200,
                                distance_text: '1.2 km',
                                address: '上海市徐汇区枫林路180号',
                                phone: '021-12345678',
                                latitude: 31.2,
                                longitude: 121.4,
                                navigation_url: 'https://example.com/nav',
                            },
                        ],
                    }),
                });
            }

            return Promise.resolve({ json: () => Promise.resolve({ success: true, sessions: [] }), ok: true });
        });

        render(<App />);

        fireEvent.click(screen.getByRole('button', { name: 'Find Nearby Hospitals' }));

        await waitFor(() => {
            expect(geolocationMock).toHaveBeenCalled();
        });

        await waitFor(() => {
            expect(mockFetch).toHaveBeenCalledWith('/api/v1/hospitals/nearby', expect.objectContaining({
                method: 'POST',
            }));
        });

        await waitFor(() => {
            expect(screen.getByText('复旦大学附属中山医院')).toBeInTheDocument();
            expect(screen.getByText('三甲医院')).toBeInTheDocument();
            expect(screen.getByText(/1.2 km/)).toBeInTheDocument();
        });
    });
});
