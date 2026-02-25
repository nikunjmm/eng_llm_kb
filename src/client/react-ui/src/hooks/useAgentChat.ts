import { useState } from 'react';
import type { Message, ActionRequest } from '@/components/chat/ChatWindow';

// Mock context for development
const MOCK_CONTEXT = {
    active_module: "Equipment Selection",
    selected_item: "PUMP-101",
    unsaved_changes: true
};

export function useAgentChat() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [isTyping, setIsTyping] = useState(false);
    const [sessionContext] = useState(MOCK_CONTEXT);

    const generateId = () => Math.random().toString(36).substring(2, 9);

    const sendMessage = async (content: string) => {
        const userMsg: Message = { id: generateId(), role: 'user', content };
        setMessages(prev => [...prev, userMsg]);
        setIsTyping(true);

        try {
            // Build the history array excluding actions for simplicity
            const history = messages.map(m => ({ role: m.role, content: m.content }));
            history.push({ role: 'user', content });

            const res = await fetch('http://localhost:8000/api/v1/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: 'dev-session',
                    messages: history,
                    csharp_context: sessionContext
                })
            });

            if (!res.ok) throw new Error('API Error');
            const data = await res.json();

            setMessages(prev => [...prev, {
                id: generateId(),
                role: 'assistant',
                content: data.text_content,
                actions: data.action_requests
            }]);
        } catch (error) {
            console.error(error);
            setMessages(prev => [...prev, {
                id: generateId(),
                role: 'system',
                content: 'Error communicating with the agent server.'
            }]);
        } finally {
            setIsTyping(false);
        }
    };

    const approveAction = (action: ActionRequest) => {
        // In a real app, this would route through the C# bridge
        console.log("Approved action routed to bridge:", action);
        const mockMsg = `I have approved and executed the action: ${action.actionName}`;
        sendMessage(mockMsg);
    };

    const rejectAction = (action: ActionRequest) => {
        const mockMsg = `I rejected the action: ${action.actionName}. Please suggest something else.`;
        sendMessage(mockMsg);
    };

    return {
        messages,
        isTyping,
        sessionContext,
        sendMessage,
        approveAction,
        rejectAction
    };
}
