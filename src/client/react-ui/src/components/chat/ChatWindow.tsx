import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { CheckIcon, XIcon, BotIcon, UserIcon } from "lucide-react";

export type ActionRequest = {
    actionName: string;
    parameters: Record<string, any>;
    reasoning: string;
    requiresApproval: boolean;
};

export type Message = {
    id: string;
    role: "user" | "assistant" | "system";
    content: string;
    actions?: ActionRequest[];
};

interface ChatWindowProps {
    messages: Message[];
    isTyping: boolean;
    onApproveAction?: (action: ActionRequest) => void;
    onRejectAction?: (action: ActionRequest) => void;
}

export function ChatWindow({ messages, isTyping, onApproveAction, onRejectAction }: ChatWindowProps) {
    return (
        <ScrollArea className="flex-1 p-4">
            <div className="space-y-6 pb-20 max-w-3xl mx-auto w-full">
                {messages.length === 0 && (
                    <div className="text-center text-muted-foreground mt-20">
                        <BotIcon className="w-12 h-12 mx-auto mb-4 opacity-20" />
                        <p className="text-lg font-medium">How can I help you today?</p>
                        <p className="text-sm mt-1">I am connected to your manufacturing application context.</p>
                    </div>
                )}

                {messages.map((message) => (
                    <div key={message.id} className={`flex gap-4 ${message.role === "user" ? "flex-row-reverse" : ""}`}>
                        <Avatar className="h-8 w-8 shrink-0">
                            {message.role === "assistant" ? (
                                <>
                                    <AvatarImage src="/bot-avatar.png" alt="AI" />
                                    <AvatarFallback className="bg-primary/10 text-primary"><BotIcon className="h-4 w-4" /></AvatarFallback>
                                </>
                            ) : (
                                <>
                                    <AvatarFallback className="bg-secondary text-secondary-foreground"><UserIcon className="h-4 w-4" /></AvatarFallback>
                                </>
                            )}
                        </Avatar>

                        <div className={`flex flex-col gap-2 max-w-[80%] ${message.role === "user" ? "items-end" : "items-start"}`}>
                            {message.content && (
                                <div className={`rounded-lg px-4 py-2 ${message.role === "user"
                                    ? "bg-primary text-primary-foreground"
                                    : "bg-muted text-foreground"
                                    }`}>
                                    <p className="text-sm whitespace-pre-wrap leading-relaxed">{message.content}</p>
                                </div>
                            )}

                            {/* Action Proposal UI */}
                            {message.actions && message.actions.length > 0 && (
                                <div className="w-full space-y-3 mt-2">
                                    {message.actions.map((action, idx) => (
                                        <Card key={idx} className="border-border/50 shadow-sm w-full">
                                            <CardHeader className="py-3 px-4 bg-muted/30 border-b">
                                                <div className="flex items-center justify-between">
                                                    <CardTitle className="text-sm font-medium flex items-center gap-2">
                                                        <Badge variant="outline" className="bg-primary/5">Proposed Action</Badge>
                                                        <code className="text-xs bg-muted px-1.5 py-0.5 rounded">{action.actionName}</code>
                                                    </CardTitle>
                                                </div>
                                            </CardHeader>
                                            <CardContent className="py-3 px-4 text-sm">
                                                <p className="text-muted-foreground mb-3">{action.reasoning}</p>
                                                <div className="bg-black/5 dark:bg-white/5 p-2 rounded text-xs font-mono overflow-x-auto">
                                                    {JSON.stringify(action.parameters, null, 2)}
                                                </div>
                                            </CardContent>
                                            {action.requiresApproval && (
                                                <CardFooter className="py-3 px-4 border-t flex gap-2 justify-end bg-muted/10">
                                                    <Button variant="outline" size="sm" onClick={() => onRejectAction?.(action)} className="h-8">
                                                        <XIcon className="w-3 h-3 mr-1" /> Reject
                                                    </Button>
                                                    <Button size="sm" onClick={() => onApproveAction?.(action)} className="h-8">
                                                        <CheckIcon className="w-3 h-3 mr-1" /> Approve & Execute
                                                    </Button>
                                                </CardFooter>
                                            )}
                                        </Card>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                ))}
                {isTyping && (
                    <div className="flex gap-4">
                        <Avatar className="h-8 w-8 shrink-0">
                            <AvatarFallback className="bg-primary/10 text-primary"><BotIcon className="h-4 w-4" /></AvatarFallback>
                        </Avatar>
                        <div className="bg-muted text-foreground rounded-lg px-4 py-3 flex items-center gap-1">
                            <span className="w-1.5 h-1.5 bg-foreground/40 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                            <span className="w-1.5 h-1.5 bg-foreground/40 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                            <span className="w-1.5 h-1.5 bg-foreground/40 rounded-full animate-bounce"></span>
                        </div>
                    </div>
                )}
            </div>
        </ScrollArea>
    );
}
