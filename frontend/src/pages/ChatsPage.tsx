import React, { useState, useRef, useEffect } from 'react';
import { Send, MoreVertical, Copy, Check, MessageSquare, Volume2, Languages, Plus, Search, Trash2 } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import Header from '../components/layout/Header';
import type { User } from '../types';

// ============= INTERFACES - Lo que tu backend debe retornar =============
interface Message {
    id: string;
    text: string;
    translation: string;
    sender: 'user' | 'ai';
    timestamp: Date;
    showTranslation: boolean;
}

interface AIFriend {
    id: string;
    name: string;
    role: string;
    avatar: string;
    level: string;
    lastMessage: string;
    timestamp: string;
    unread: boolean;
}

// ============= SERVICIOS - Aquí conectarás tu backend =============
class ChatService {
    private apiUrl: string;

    constructor(apiUrl: string = '/api') {
        this.apiUrl = apiUrl;
    }

    // Obtener lista de amigos IA del usuario
    async getAIFriends(userId: string): Promise<AIFriend[]> {
        // TODO: Reemplazar con tu llamada real
        // const response = await fetch(`${this.apiUrl}/users/${userId}/ai-friends`);
        // return response.json();

        // Mock data por ahora
        return [
            {
                id: '1',
                name: 'Sarah',
                role: 'Medical Sales Rep',
                avatar: '👩‍⚕️',
                level: 'A2',
                lastMessage: 'How was your meeting?',
                timestamp: 'hace 2 horas',
                unread: true
            },
            {
                id: '2',
                name: 'Mike',
                role: 'Gym Trainer',
                avatar: '💪',
                level: 'A2',
                lastMessage: 'Ready for leg day?',
                timestamp: 'hace 5 horas',
                unread: false
            },
            {
                id: '3',
                name: 'Emma',
                role: 'Travel Companion',
                avatar: '✈️',
                level: 'A2',
                lastMessage: 'Where should we go next?',
                timestamp: 'ayer',
                unread: false
            },
            {
                id: '4',
                name: 'Dr. James',
                role: 'Doctor',
                avatar: '👨‍⚕️',
                level: 'A2',
                lastMessage: 'Take care!',
                timestamp: 'hace 2 días',
                unread: false
            }
        ];
    }

    // Obtener mensajes de una conversación
    async getMessages(userId: string, friendId: string): Promise<Message[]> {
        // TODO: Reemplazar con tu llamada real
        // const response = await fetch(`${this.apiUrl}/users/${userId}/conversations/${friendId}/messages`);
        // return response.json();

        // Mock data por ahora
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

    // Enviar mensaje y obtener respuesta de la IA
    async sendMessage(
        userId: string,
        friendId: string,
        message: string,
        targetLanguage: string,
        userLanguage: string
    ): Promise<Message> {
        // TODO: Reemplazar con tu llamada real
        // const response = await fetch(`${this.apiUrl}/users/${userId}/conversations/${friendId}/messages`, {
        //   method: 'POST',
        //   headers: { 'Content-Type': 'application/json' },
        //   body: JSON.stringify({ message, targetLanguage, userLanguage })
        // });
        // return response.json();

        // Mock: Simular delay de red
        await new Promise(resolve => setTimeout(resolve, 1500 + Math.random() * 1000));

        // Mock response
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

    // Traducir un mensaje
    async translateMessage(text: string, targetLanguage: string): Promise<string> {
        // TODO: Reemplazar con tu llamada real
        return `(Traducción de: "${text}")`;
    }

    // Corregir gramática del mensaje del usuario
    async correctMessage(text: string, targetLanguage: string): Promise<{ original: string; corrected: string; explanation: string }> {
        // TODO: Reemplazar con tu llamada real
        return {
            original: text,
            corrected: text,
            explanation: 'Tu mensaje está correcto!'
        };
    }

    // Obtener comentario/feedback sobre el mensaje
    async getMessageFeedback(text: string, context: string): Promise<string> {
        // TODO: Reemplazar con tu llamada real
        return 'Good use of vocabulary! Try using more complex sentence structures.';
    }

    // Text-to-speech
    async speakMessage(text: string, language: string): Promise<void> {
        // TODO: Implementar con Web Speech API o servicio backend
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = language === 'es' ? 'es-ES' : 'en-US';
            speechSynthesis.speak(utterance);
        }
    }
}

// ============= COMPONENTE PRINCIPAL =============
// Props opcionales para configuración avanzada
interface LanguageChatAppProps {
    apiUrl?: string;
}

const LanguageChatApp: React.FC<LanguageChatAppProps> = ({
    apiUrl = '/api',
}) => {
    // Obtener usuario del contexto
    const { user, loading, isAuthenticated } = useAuth();

    // Derivar configuración del usuario o usar defaults/overrides
    const userId = user?.id ? String(user.id) : null;
    const targetLanguage = user?.learning_profile?.target_language;
    const userLanguage = user?.learning_profile?.native_language;
    const userLevel = user?.learning_profile?.cefr_level;

    const chatServiceRef = useRef(new ChatService(apiUrl));
    const chatService = chatServiceRef.current;

    const [aiFriends, setAIFriends] = useState<AIFriend[]>([]);
    const [selectedFriend, setSelectedFriend] = useState<AIFriend | null>(null);
    const [messages, setMessages] = useState<Message[]>([]);
    const [inputText, setInputText] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [activeMenu, setActiveMenu] = useState<string | null>(null);
    const [activeSidebarMenu, setActiveSidebarMenu] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Cargar amigos IA cuando el usuario esté disponible
    useEffect(() => {
        if (!loading && isAuthenticated && userId) {
            loadAIFriends();
        }
    }, [loading, isAuthenticated, userId]);

    // Cargar mensajes cuando se selecciona un amigo
    useEffect(() => {
        if (selectedFriend && userId) {
            loadMessages(selectedFriend.id);
        }
    }, [selectedFriend?.id]);

    const loadAIFriends = async () => {
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
    };

    const loadMessages = async (friendId: string) => {
        if (!userId) return;

        try {
            const msgs = await chatService.getMessages(userId, friendId);
            setMessages(msgs);
        } catch (err) {
            console.error('Error loading messages:', err);
            setError('Error al cargar mensajes');
        }
    };

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Cerrar menú al hacer clic fuera
    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            const target = event.target as HTMLElement;

            // Cerrar menú de mensajes
            if (activeMenu) {
                if (!target.closest('.message-menu') && !target.closest('.menu-button')) {
                    setActiveMenu(null);
                }
            }

            // Cerrar menú del sidebar
            if (activeSidebarMenu) {
                if (!target.closest('.sidebar-menu') && !target.closest('.more-button')) {
                    setActiveSidebarMenu(null);
                }
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [activeMenu, activeSidebarMenu]);

    const handleSendMessage = async () => {
        if (!inputText.trim() || !selectedFriend || !userId) return;

        const userMessage: Message = {
            id: `temp-${Date.now()}`,
            text: inputText,
            translation: await chatService.translateMessage(inputText, userLanguage),
            sender: 'user',
            timestamp: new Date(),
            showTranslation: true
        };

        setMessages(prev => [...prev, userMessage]);
        setInputText('');
        setIsTyping(true);

        try {
            const aiMessage = await chatService.sendMessage(
                userId,
                selectedFriend.id,
                inputText,
                targetLanguage,
                userLanguage
            );

            setMessages(prev => [...prev, aiMessage]);
        } catch (err) {
            console.error('Error sending message:', err);
            setError('Error al enviar mensaje');
        } finally {
            setIsTyping(false);
        }
    };

    const toggleTranslation = (messageId: string) => {
        setMessages(prev =>
            prev.map(msg =>
                msg.id === messageId
                    ? { ...msg, showTranslation: !msg.showTranslation }
                    : msg
            )
        );
        setActiveMenu(null);
    };

    const copyMessage = (text: string) => {
        navigator.clipboard.writeText(text);
        setActiveMenu(null);
    };

    const handleCorrectMessage = async (message: Message) => {
        try {
            const correction = await chatService.correctMessage(message.text, targetLanguage);
            alert(`Original: ${correction.original}\nCorrección: ${correction.corrected}\n\n${correction.explanation}`);
        } catch (err) {
            console.error('Error correcting message:', err);
        }
        setActiveMenu(null);
    };

    const handleGetFeedback = async (message: Message) => {
        try {
            const feedback = await chatService.getMessageFeedback(message.text, selectedFriend?.role || '');
            alert(feedback);
        } catch (err) {
            console.error('Error getting feedback:', err);
        }
        setActiveMenu(null);
    };

    const handleSpeak = async (text: string) => {
        try {
            await chatService.speakMessage(text, targetLanguage);
        } catch (err) {
            console.error('Error speaking message:', err);
        }
        setActiveMenu(null);
    };

    const handleDeleteChat = async (e: React.MouseEvent, friendId: string) => {
        e.stopPropagation(); // Evitar seleccionar el chat al borrar
        if (window.confirm('¿Estás seguro de que quieres eliminar esta conversación?')) {
            // TODO: Implementar llamada al backend
            setAIFriends(prev => prev.filter(f => f.id !== friendId));
            if (selectedFriend?.id === friendId) {
                setSelectedFriend(null);
            }
        }
    };

    // Estado de error o sin autenticación
    if (error && !userId) {
        return (
            <div className="flex items-center justify-center h-screen bg-gray-50">
                <div className="text-center">
                    <p className="text-red-500 mb-4">{error}</p>
                    <button
                        onClick={() => window.location.reload()}
                        className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
                    >
                        Reintentar
                    </button>
                </div>
            </div>
        );
    }

    if (isLoading) {
        return (
            <div className="flex items-center justify-center h-screen bg-gray-50">
                <div className="text-gray-500">Cargando conversaciones...</div>
            </div>
        );
    }

    return (
        <div className="flex flex-col h-screen bg-gray-50">
            {/* Header Global */}
            <Header showStats={true} />

            {/* Contenido Principal (Chat) - Restamos la altura del header (64px) */}
            <div className="flex flex-1 overflow-hidden h-[calc(100vh-64px)]">
                {/* Sidebar - Lista de Chats */}
                <div className="w-80 bg-white border-r border-gray-200 flex flex-col">
                    <div className="p-4 border-b border-gray-200">
                        <div className="flex items-center justify-between mb-4">
                            <h1 className="text-2xl font-bold text-gray-800">Chats</h1>
                            <button className="p-2 hover:bg-gray-100 rounded-full transition">
                                <Plus className="w-5 h-5 text-gray-600" />
                            </button>
                        </div>
                        <div className="relative">
                            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                            <input
                                type="text"
                                placeholder="Buscar conversaciones..."
                                className="w-full pl-10 pr-4 py-2 bg-gray-100 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                            />
                        </div>
                        {/* Mostrar nivel del usuario */}
                        <div className="mt-2 text-xs text-gray-500">
                            Practicando {targetLanguage.toUpperCase()} • Nivel {userLevel}
                        </div>
                    </div>

                    <div className="flex-1 overflow-y-auto">
                        {aiFriends.map(friend => (
                            <div
                                key={friend.id}
                                onClick={() => setSelectedFriend(friend)}
                                className={`p-4 border-b border-gray-100 cursor-pointer transition group ${selectedFriend?.id === friend.id
                                    ? 'bg-blue-50 border-l-4 border-l-blue-500'
                                    : 'hover:bg-gray-50'
                                    }`}
                            >
                                <div className="flex items-start gap-3">
                                    <div className="text-3xl">{friend.avatar}</div>
                                    <div className="flex-1 min-w-0">
                                        <div className="flex items-center justify-between">
                                            <h3 className="font-semibold text-gray-800 truncate">
                                                {friend.name}
                                            </h3>
                                            <span className="text-xs text-gray-500">{friend.timestamp}</span>
                                        </div>
                                        <p className="text-xs text-blue-600 font-medium mb-1">
                                            {friend.role} • Nivel {friend.level}
                                        </p>
                                        <p className="text-sm text-gray-600 truncate">
                                            {friend.lastMessage}
                                        </p>
                                    </div>
                                    <div className="flex flex-col items-end gap-2 relative">
                                        {friend.unread && (
                                            <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                                        )}
                                        <div className="relative">
                                            <button
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    setActiveSidebarMenu(activeSidebarMenu === friend.id ? null : friend.id);
                                                }}
                                                className={`more-button p-1 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-full transition ${activeSidebarMenu === friend.id ? 'opacity-100' : 'opacity-30 group-hover:opacity-100'}`}
                                            >
                                                <MoreVertical className="w-4 h-4" />
                                            </button>

                                            {activeSidebarMenu === friend.id && (
                                                <div className="absolute right-0 top-6 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-20 w-32 sidebar-menu">
                                                    <button
                                                        onClick={(e) => handleDeleteChat(e, friend.id)}
                                                        className="w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-50 flex items-center gap-2"
                                                    >
                                                        <Trash2 className="w-4 h-4" />
                                                        Eliminar
                                                    </button>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Área de Chat Principal */}
                <div className="flex-1 flex flex-col">
                    {selectedFriend ? (
                        <>
                            {/* Header del Chat */}
                            <div className="bg-white border-b border-gray-200 p-4">
                                <div className="flex items-center gap-3">
                                    <div className="text-4xl">{selectedFriend.avatar}</div>
                                    <div>
                                        <h2 className="font-bold text-gray-800">{selectedFriend.name}</h2>
                                        <p className="text-sm text-gray-600">
                                            {selectedFriend.role} • Practicando nivel {selectedFriend.level}
                                        </p>
                                    </div>
                                </div>
                            </div>

                            {/* Mensajes */}
                            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                                {messages.map(message => (
                                    <div
                                        key={message.id}
                                        className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                                    >
                                        {/* La burbuja del mensaje */}
                                        <div className={`relative group max-w-md`}>
                                            <div
                                                className={`rounded-2xl px-4 py-3 ${message.sender === 'user'
                                                    ? 'bg-blue-500 text-white'
                                                    : 'bg-gray-200 text-gray-800'
                                                    }`}
                                            >
                                                <p className="text-sm mb-1">{message.text}</p>
                                                {message.showTranslation && (
                                                    <p className={`text-xs mt-2 pt-2 border-t ${message.sender === 'user'
                                                        ? 'border-blue-400 text-blue-100'
                                                        : 'border-gray-300 text-gray-600'
                                                        }`}>
                                                        {message.translation}
                                                    </p>
                                                )}
                                            </div>

                                            {/* Menú contextual */}
                                            <button
                                                onClick={() => setActiveMenu(activeMenu === message.id ? null : message.id)}
                                                className={`menu-button absolute ${message.sender === 'user' ? '-left-10' : '-right-10'} top-2 opacity-0 group-hover:opacity-100 p-1 hover:bg-gray-100 rounded transition`}
                                            >
                                                <MoreVertical className="w-4 h-4 text-gray-600" />
                                            </button>

                                            {activeMenu === message.id && (
                                                <div className={`message-menu absolute ${message.sender === 'user' ? '-left-52' : '-right-52'} top-0 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-10 w-48`}>
                                                    <button
                                                        onClick={() => copyMessage(message.text)}
                                                        className="w-full px-4 py-2 text-left text-sm hover:bg-gray-50 flex items-center gap-2"
                                                    >
                                                        <Copy className="w-4 h-4" /> Copiar
                                                    </button>
                                                    {message.sender === 'user' && (
                                                        <button
                                                            onClick={() => handleCorrectMessage(message)}
                                                            className="w-full px-4 py-2 text-left text-sm hover:bg-gray-50 flex items-center gap-2"
                                                        >
                                                            <Check className="w-4 h-4" /> Corregir
                                                        </button>
                                                    )}
                                                    <button
                                                        onClick={() => handleGetFeedback(message)}
                                                        className="w-full px-4 py-2 text-left text-sm hover:bg-gray-50 flex items-center gap-2"
                                                    >
                                                        <MessageSquare className="w-4 h-4" /> Comentario
                                                    </button>
                                                    <button
                                                        onClick={() => handleSpeak(message.text)}
                                                        className="w-full px-4 py-2 text-left text-sm hover:bg-gray-50 flex items-center gap-2"
                                                    >
                                                        <Volume2 className="w-4 h-4" /> Hablar
                                                    </button>
                                                    <button
                                                        onClick={() => toggleTranslation(message.id)}
                                                        className="w-full px-4 py-2 text-left text-sm hover:bg-gray-50 flex items-center gap-2"
                                                    >
                                                        <Languages className="w-4 h-4" />
                                                        {message.showTranslation ? 'Ocultar' : 'Mostrar'} traducción
                                                    </button>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                ))}

                                {isTyping && (
                                    <div className="flex justify-start">
                                        <div className="bg-gray-200 rounded-2xl px-4 py-3">
                                            <div className="flex gap-1">
                                                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                                                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                                                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                                            </div>
                                        </div>
                                    </div>
                                )}

                                <div ref={messagesEndRef} />
                            </div>

                            {/* Input de Mensaje */}
                            <div className="bg-white border-t border-gray-200 p-4">
                                <div className="flex gap-2">
                                    <input
                                        type="text"
                                        value={inputText}
                                        onChange={e => setInputText(e.target.value)}
                                        onKeyPress={e => e.key === 'Enter' && handleSendMessage()}
                                        placeholder="Escribe tu mensaje..."
                                        className="flex-1 px-4 py-3 bg-gray-100 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    />
                                    <button
                                        onClick={handleSendMessage}
                                        disabled={!inputText.trim()}
                                        className="bg-blue-500 text-white p-3 rounded-full hover:bg-blue-600 transition disabled:opacity-50 disabled:cursor-not-allowed"
                                    >
                                        <Send className="w-5 h-5" />
                                    </button>
                                </div>
                            </div>
                        </>
                    ) : (
                        <div className="flex-1 flex items-center justify-center text-gray-500">
                            Selecciona una conversación para comenzar
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default LanguageChatApp;