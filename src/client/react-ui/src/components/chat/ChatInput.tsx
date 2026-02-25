import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { SendIcon } from "lucide-react";

interface ChatInputProps {
    onSendMessage: (message: string) => void;
    disabled?: boolean;
}

export function ChatInput({ onSendMessage, disabled }: ChatInputProps) {
    const [input, setInput] = useState("");

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (input.trim() && !disabled) {
            onSendMessage(input.trim());
            setInput("");
        }
    };

    return (
        <form
            onSubmit={handleSubmit}
            className="p-4 bg-background border-t flex items-center gap-2"
        >
            <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask the Engineering Assistant..."
                disabled={disabled}
                className="flex-1"
                autoFocus
            />
            <Button type="submit" size="icon" disabled={disabled || !input.trim()}>
                <SendIcon className="h-4 w-4" />
            </Button>
        </form>
    );
}
