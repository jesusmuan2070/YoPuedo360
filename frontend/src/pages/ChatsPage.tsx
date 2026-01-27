/**
 * ChatPage - Componente principal de la página de chat
 * 
 * Este componente SOLO maneja:
 * - Estructura JSX
 * - Layout visual
 * - Renderizado condicional
 * 
 * TODA la lógica está en useChatLogic hook
 */

import React from 'react';
import { Send, MoreVertical, Copy, Check, MessageSquare, Volume2, Languages, Plus, Search, Trash2 } from 'lucide-react';
import Header from '../components/layout/Header';
import { useChatLogic, AIFriend } from '../hooks/useChatLogic';
import { formatDistanceToNow, format, isYesterday, isThisWeek } from 'date-fns';
import { es } from 'date-fns/locale';

// Función para formatear fechas de manera amigable
const formatTimestamp = (date: Date) => {
    const now = new Date();
    const diff = now.getTime() - date.getTime();

    // Si es hoy (menos de 24h aprox y NO es ayer)
    if (diff < 86400000 && !isYesterday(date)) {
        if (diff < 60000) return 'ahora';
        return formatDistanceToNow(date, { addSuffix: true, locale: es });
    }

    // Si fue ayer
    if (isYesterday(date)) {
        return 'Ayer';
    }

    // Si es de esta semana (ej: "lunes", "martes")
    if (isThisWeek(date, { weekStartsOn: 1 })) {
        return format(date, 'EEEE', { locale: es });
    }

    // Si es más viejo, mostrar fecha corta
    return format(date, 'd MMM', { locale: es });
};

const ChatPage: React.FC = () => {
    // ✅ UNA LÍNEA: Importar toda la lógica del hook
    const {
        // Auth
        authLoading,
        isAuthenticated,
        user,
        targetLanguage,
        userLevel,

        // Estado
        aiFriends,
        selectedFriend,
        messages,
        inputText,
        isTyping,
        activeMenu,
        activeSidebarMenu,
        isLoading,
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
    } = useChatLogic();

    // ========== RENDER CONDICIONAL ==========
    // Loading de autenticación
    if (authLoading) {
        return (
            <div className="flex items-center justify-center h-screen bg-gray-50">
                <div className="text-gray-500">Cargando usuario...</div>
            </div>
        );
    }

    // No autenticado
    if (!isAuthenticated || !user) {
        return (
            <div className="flex items-center justify-center h-screen bg-gray-50">
                <div className="text-center">
                    <p className="text-red-500 mb-4">Debes iniciar sesión para acceder al chat</p>
                    <button
                        onClick={() => window.location.href = '/login'}
                        className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
                    >
                        Ir a Login
                    </button>
                </div>
            </div>
        );
    }

    // Loading de conversaciones
    if (isLoading) {
        return (
            <div className="flex items-center justify-center h-screen bg-gray-50">
                <div className="text-gray-500">Cargando conversaciones...</div>
            </div>
        );
    }

    // ========== UI PRINCIPAL (SOLO JSX) ==========
    return (
        <div className="flex flex-col h-screen bg-gray-50">
            {/* Header Global */}
            <Header showStats={true} />

            {/* Contenido Principal (Chat) */}
            <div className="flex flex-1 overflow-hidden h-[calc(100vh-64px)]">
                {/* ==================== SIDEBAR ==================== */}
                <div className="w-80 bg-white border-r border-gray-200 flex flex-col">
                    {/* Header del Sidebar */}
                    <div className="p-4 border-b border-gray-200">
                        <div className="flex items-center justify-between mb-4">
                            <h1 className="text-2xl font-bold text-gray-800">
                                Chats
                                {totalUnreadCount > 0 && (
                                    <span className="ml-2 text-sm bg-blue-500 text-white rounded-full px-2 py-0.5">
                                        {totalUnreadCount}
                                    </span>
                                )}
                            </h1>
                            <button className="p-2 hover:bg-gray-100 rounded-full transition">
                                <Plus className="w-5 h-5 text-gray-600" />
                            </button>
                        </div>

                        {/* Barra de búsqueda */}
                        <div className="relative">
                            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                            <input
                                type="text"
                                placeholder="Buscar conversaciones..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="w-full pl-10 pr-4 py-2 bg-gray-100 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                            />
                        </div>

                        {/* Info del usuario */}
                        <div className="mt-2 text-xs text-gray-500">
                            Practicando {targetLanguage.toUpperCase()} • Nivel {userLevel}
                        </div>
                    </div>

                    {/* Lista de conversaciones */}
                    <div className="flex-1 overflow-y-auto">
                        {aiFriends.length === 0 ? (
                            <div className="p-4 text-center text-gray-500">
                                {searchQuery ? 'No se encontraron conversaciones' : 'No hay conversaciones'}
                            </div>
                        ) : (
                            aiFriends.map(friend => (
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
                                                <span className="text-xs text-gray-500">
                                                    {formatTimestamp(friend.timestamp)}
                                                </span>
                                            </div>
                                            <p className="text-xs text-blue-600 font-medium mb-1">
                                                {friend.role} • Nivel {friend.level}
                                            </p>
                                            <div className="flex items-center justify-between">
                                                <p className="text-sm text-gray-600 truncate flex-1">
                                                    {friend.lastMessage}
                                                </p>
                                                {friend.unreadCount > 0 && (
                                                    <span className="ml-2 bg-blue-500 text-white text-xs rounded-full px-2 py-0.5">
                                                        {friend.unreadCount}
                                                    </span>
                                                )}
                                            </div>
                                        </div>

                                        {/* Menú de 3 puntos */}
                                        <div className="flex flex-col items-end gap-2 relative">
                                            <button
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    setActiveSidebarMenu(activeSidebarMenu === friend.id ? null : friend.id);
                                                }}
                                                className={`more-button p-1 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-full transition ${activeSidebarMenu === friend.id ? 'opacity-100' : 'opacity-0 group-hover:opacity-100'
                                                    }`}
                                            >
                                                <MoreVertical className="w-4 h-4" />
                                            </button>

                                            {activeSidebarMenu === friend.id && (
                                                <div className="sidebar-menu absolute right-0 top-6 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-20 w-32">
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
                            ))
                        )}
                    </div>
                </div>

                {/* ==================== ÁREA DE CHAT ==================== */}
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

                            {/* Lista de Mensajes */}
                            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                                {messages.map(message => (
                                    <div
                                        key={message.id}
                                        className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                                    >
                                        <div className="relative group max-w-md">
                                            {/* Burbuja del mensaje */}
                                            <div
                                                className={`rounded-2xl px-4 py-3 ${message.sender === 'user'
                                                    ? 'bg-blue-500 text-white'
                                                    : 'bg-gray-200 text-gray-800'
                                                    }`}
                                            >
                                                <p className="text-sm mb-1">{message.text}</p>
                                                {message.showTranslation && message.translation && (
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
                                                className={`menu-button absolute ${message.sender === 'user' ? '-left-10' : '-right-10'
                                                    } top-2 opacity-0 group-hover:opacity-100 p-1 hover:bg-gray-100 rounded transition`}
                                            >
                                                <MoreVertical className="w-4 h-4 text-gray-600" />
                                            </button>

                                            {activeMenu === message.id && (
                                                <div className={`message-menu absolute ${message.sender === 'user' ? '-left-52' : '-right-52'
                                                    } top-0 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-10 w-48`}>
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

                                {/* Indicador de "escribiendo..." */}
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

export default ChatPage;