/**
 * useChatLogic - Custom hook que contiene TODA la lógica de negocio del chat
 */

import { useState, useEffect, useRef, useCallback, useMemo } from 'react';

import { useAuth } from '../context/AuthContext';
import { formatDistanceToNow, format } from 'date-fns';
import { es } from 'date-fns/locale';

// ============= INTERFACES =============
export interface Message {
    id: string;
    text: string;
    translation: string;
    sender: 'user' | 'ai';
    timestamp: Date;
    showTranslation: boolean;
}

export interface AIFriend {
    id: string;
    name: string;
    role: string;
    avatar: string;
    level: string;
    lastMessage: string;
    timestamp: Date; // Cambiado a Date real para el cálculo relativo
    unread: boolean;
    unreadCount: number;
}

interface CorrectionResult {
    original: string;
    corrected: string;
    explanation: string;
}

// ============= CHAT SERVICE =============
class ChatService {
    private apiUrl: string;

    constructor(apiUrl: string = '/api') {
        this.apiUrl = apiUrl;
    }

    async getAIFriends(userId: string): Promise<AIFriend[]> {
        // TODO: Reemplazar con llamada real
        // const response = await fetch(`${this.apiUrl}/users/${userId}/ai-friends`);
        // return response.json();

        return [
            {
                id: '1',
                name: 'Sarah',
                role: 'Medical Sales Rep',
                avatar: '👩‍⚕️',
                level: 'A2',
                lastMessage: 'How was your meeting?',
                timestamp: new Date(Date.now() - 600000), // Hace 10 minutos (debería decir "hace 10 minutos")
                unread: true,
                unreadCount: 3
            },
            {
                id: '2',
                name: 'Mike',
                role: 'Gym Trainer',
                avatar: '💪',
                level: 'A2',
                lastMessage: 'Ready for leg day?',
                timestamp: new Date(Date.now() - 259200000), // Hace 3 días (debería decir "sábado" o el día que sea)
                unread: false,
                unreadCount: 0
            },
            {
                id: '3',
                name: 'Emma',
                role: 'Travel Companion',
                avatar: '✈️',
                level: 'A2',
                lastMessage: 'Where should we go next?',
                timestamp: new Date(Date.now() - 864000000), // Hace 10 días (debería decir la fecha ej: "17 ene")
                unread: true,
                unreadCount: 1
            }
        ];
    }

    async getMessages(userId: string, friendId: string): Promise<Message[]> {
        // TODO: Reemplazar con llamada real
        return [
            {
                id: '1',
                text: 'Hey! How are you today?',
                translation: '¡Hola! ¿Cómo estás hoy?',
                sender: 'ai',
                timestamp: new Date(Date.now() - 3600000),
                showTranslation: true
            },
            {
                id: '2',
                text: 'I am good, thanks!',
                translation: 'Estoy bien, ¡gracias!',
                sender: 'user',
                timestamp: new Date(Date.now() - 3500000),
                showTranslation: true
            }
        ];
    }

    async sendMessage(
        userId: string,
        friendId: string,
        message: string,
        targetLanguage: string,
        userLanguage: string
    ): Promise<Message> {
        // TODO: Reemplazar con llamada real
        await new Promise(resolve => setTimeout(resolve, 1500));

        const responses = [
            { text: 'That sounds interesting! Tell me more.', translation: '¡Eso suena interesante! Cuéntame más.' },
            { text: 'I understand. How can I help?', translation: 'Entiendo. ¿Cómo puedo ayudar?' },
            { text: 'Great! What do you think about that?', translation: '¡Genial! ¿Qué opinas de eso?' }
        ];

        const randomResponse = responses[Math.floor(Math.random() * responses.length)];

        return {
            id: Date.now().toString(),
            text: randomResponse.text,
            translation: randomResponse.translation,
            sender: 'ai',
            timestamp: new Date(),
            showTranslation: true
        };
    }

    async translateMessage(text: string, targetLanguage: string): Promise<string> {
        // TODO: Reemplazar con llamada real
        return `(Traducción de: "${text}")`;
    }

    async correctMessage(text: string, targetLanguage: string): Promise<CorrectionResult> {
        // TODO: Reemplazar con llamada real
        return {
            original: text,
            corrected: text,
            explanation: 'Tu mensaje está correcto!'
        };
    }

    async getMessageFeedback(text: string, context: string): Promise<string> {
        // TODO: Reemplazar con llamada real
        return 'Good use of vocabulary! Try using more complex sentence structures.';
    }

    async speakMessage(text: string, language: string): Promise<void> {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = language === 'es' ? 'es-ES' : 'en-US';
            speechSynthesis.speak(utterance);
        }
    }

    async markAsRead(userId: string, friendId: string): Promise<void> {
        // TODO: Reemplazar con llamada real al backend
        // await fetch(`${this.apiUrl}/users/${userId}/conversations/${friendId}/read`, { method: 'POST' });
        console.log(`Marking chat ${friendId} as read for user ${userId}`);
    }
}

// ============= CUSTOM HOOK =============
export const useChatLogic = (apiUrl: string = '/api') => {
    // Auth
    const { user, loading: authLoading, isAuthenticated } = useAuth();

    // Derivar info del usuario
    const userId = user?.id ? String(user.id) : null;
    const targetLanguage = user?.learning_profile?.target_language || 'en';
    const userLanguage = user?.learning_profile?.native_language || 'es';
    const userLevel = user?.learning_profile?.cefr_level || 'A2';

    // Service - usar useMemo en lugar de useRef para TypeScript
    const chatService = useMemo(() => new ChatService(apiUrl), [apiUrl]);

    // ========== ESTADOS ==========
    const [aiFriends, setAIFriends] = useState<AIFriend[]>([]);
    const [selectedFriend, setSelectedFriend] = useState<AIFriend | null>(null);
    const [messages, setMessages] = useState<Message[]>([]);
    const [inputText, setInputText] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [activeMenu, setActiveMenu] = useState<string | null>(null);
    const [activeSidebarMenu, setActiveSidebarMenu] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [searchQuery, setSearchQuery] = useState('');

    // Referencias
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // ========== COMPUTED VALUES ==========
    // Filtrar amigos según búsqueda
    const filteredFriends = useMemo(() => {
        if (!searchQuery) return aiFriends;

        const query = searchQuery.toLowerCase();
        return aiFriends.filter(friend =>
            friend.name.toLowerCase().includes(query) ||
            friend.role.toLowerCase().includes(query) ||
            friend.lastMessage.toLowerCase().includes(query)
        );
    }, [aiFriends, searchQuery]);

    // Calcular total de no leídos
    const totalUnreadCount = useMemo(() => {
        return aiFriends.reduce((sum, f) => sum + f.unreadCount, 0);
    }, [aiFriends]);

    // ========== FUNCIONES DE CARGA ==========
    const loadAIFriends = useCallback(async () => {
        if (!userId) return;

        try {
            setIsLoading(true);
            setError(null);
            const friends = await chatService.getAIFriends(userId);
            setAIFriends(friends);

            if (friends.length > 0 && !selectedFriend) {
                setSelectedFriend(friends[0]);
            }
        } catch (err) {
            console.error('Error loading AI friends:', err);
            setError('Error al cargar conversaciones');
        } finally {
            setIsLoading(false);
        }
    }, [userId, chatService, selectedFriend]);

    const loadMessages = useCallback(async (friendId: string) => {
        if (!userId) return;

        try {
            const msgs = await chatService.getMessages(userId, friendId);
            setMessages(msgs);
        } catch (err) {
            console.error('Error loading messages:', err);
            setError('Error al cargar mensajes');
        }
    }, [userId, chatService]);

    // ========== HANDLERS ==========
    const handleSendMessage = useCallback(async () => {
        if (!inputText.trim() || !selectedFriend || !userId) return;

        const messageText = inputText;

        const userMessage: Message = {
            id: `temp-${Date.now()}`,
            text: messageText,
            translation: '',
            sender: 'user',
            timestamp: new Date(),
            showTranslation: true
        };

        setMessages(prev => [...prev, userMessage]);
        setInputText('');
        setIsTyping(true);

        try {
            const translation = await chatService.translateMessage(messageText, userLanguage);

            setMessages(prev =>
                prev.map(msg =>
                    msg.id === userMessage.id ? { ...msg, translation } : msg
                )
            );

            const aiMessage = await chatService.sendMessage(
                userId,
                selectedFriend.id,
                messageText,
                targetLanguage,
                userLanguage
            );

            setMessages(prev => [...prev, aiMessage]);
        } catch (err) {
            console.error('Error sending message:', err);
            setError('Error al enviar mensaje');
            setMessages(prev => prev.filter(msg => msg.id !== userMessage.id));
        } finally {
            setIsTyping(false);
        }
    }, [inputText, selectedFriend, userId, chatService, targetLanguage, userLanguage]);

    const handleDeleteChat = useCallback((e: React.MouseEvent, friendId: string) => {
        e.stopPropagation();
        if (window.confirm('¿Estás seguro de que quieres eliminar esta conversación?')) {
            setAIFriends(prev => prev.filter(f => f.id !== friendId));
            if (selectedFriend?.id === friendId) {
                setSelectedFriend(null);
            }
        }
    }, [selectedFriend]);

    const toggleTranslation = useCallback((messageId: string) => {
        setMessages(prev =>
            prev.map(msg =>
                msg.id === messageId ? { ...msg, showTranslation: !msg.showTranslation } : msg
            )
        );
        setActiveMenu(null);
    }, []);

    const copyMessage = useCallback((text: string) => {
        navigator.clipboard.writeText(text);
        setActiveMenu(null);
    }, []);

    const handleCorrectMessage = useCallback(async (message: Message) => {
        try {
            const correction = await chatService.correctMessage(message.text, targetLanguage);
            alert(`Original: ${correction.original}\nCorrección: ${correction.corrected}\n\n${correction.explanation}`);
        } catch (err) {
            console.error('Error correcting message:', err);
        }
        setActiveMenu(null);
    }, [chatService, targetLanguage]);

    const handleGetFeedback = useCallback(async (message: Message) => {
        try {
            const feedback = await chatService.getMessageFeedback(message.text, selectedFriend?.role || '');
            alert(feedback);
        } catch (err) {
            console.error('Error getting feedback:', err);
        }
        setActiveMenu(null);
    }, [chatService, selectedFriend]);

    const handleSpeak = useCallback(async (text: string) => {
        try {
            await chatService.speakMessage(text, targetLanguage);
        } catch (err) {
            console.error('Error speaking message:', err);
        }
        setActiveMenu(null);
    }, [chatService, targetLanguage]);

    const scrollToBottom = useCallback(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, []);

    const markAsRead = useCallback(async (friendId: string) => {
        if (!userId) return;
        try {
            await chatService.markAsRead(userId, friendId);
            // Actualizar estado local
            setAIFriends(prev => prev.map(f =>
                f.id === friendId
                    ? { ...f, unread: false, unreadCount: 0 }
                    : f
            ));
        } catch (err) {
            console.error('Error marking as read:', err);
        }
    }, [userId, chatService]);

    // ========== EFFECTS ==========
    useEffect(() => {
        if (!authLoading && isAuthenticated && userId) {
            loadAIFriends();
        }
    }, [authLoading, isAuthenticated, userId, loadAIFriends]);

    useEffect(() => {
        if (selectedFriend && userId) {
            loadMessages(selectedFriend.id);
            markAsRead(selectedFriend.id);
        }
    }, [selectedFriend?.id, userId, loadMessages, markAsRead]);

    useEffect(() => {
        scrollToBottom();
    }, [messages, scrollToBottom]);

    useEffect(() => {
        document.title = totalUnreadCount > 0
            ? `(${totalUnreadCount}) Chat | YoPuedo360`
            : 'Chat | YoPuedo360';
    }, [totalUnreadCount]);

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            const target = event.target as HTMLElement;

            if (activeMenu && !target.closest('.message-menu') && !target.closest('.menu-button')) {
                setActiveMenu(null);
            }

            if (activeSidebarMenu && !target.closest('.sidebar-menu') && !target.closest('.more-button')) {
                setActiveSidebarMenu(null);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, [activeMenu, activeSidebarMenu]);

    // ========== RETORNAR TODO ==========
    return {
        // Auth state
        user,
        authLoading,
        isAuthenticated,
        userId,
        targetLanguage,
        userLanguage,
        userLevel,

        // Chat state
        aiFriends: filteredFriends,
        selectedFriend,
        messages,
        inputText,
        isTyping,
        activeMenu,
        activeSidebarMenu,
        isLoading,
        error,
        searchQuery,
        totalUnreadCount,
        messagesEndRef,

        // Setters
        setSelectedFriend,
        setInputText,
        setActiveMenu,
        setActiveSidebarMenu,
        setSearchQuery,

        // Handlers
        handleSendMessage,
        handleDeleteChat,
        toggleTranslation,
        copyMessage,
        handleCorrectMessage,
        handleGetFeedback,
        handleSpeak,
        scrollToBottom,
    };
};