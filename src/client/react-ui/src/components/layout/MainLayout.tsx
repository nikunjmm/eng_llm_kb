import React from "react";

interface MainLayoutProps {
    children: React.ReactNode;
    contextPanel: React.ReactNode;
}

export function MainLayout({ children, contextPanel }: MainLayoutProps) {
    return (
        <div className="flex h-screen w-full bg-background overflow-hidden">
            {/* Left Sidebar (History/Nav) */}
            <div className="w-64 border-r bg-muted/20 flex flex-col">
                <div className="p-4 border-b font-semibold tracking-tight text-lg">
                    Eng RAG
                </div>
                <div className="flex-1 p-4 text-sm text-muted-foreground">
                    <p>Session history will appear here.</p>
                </div>
            </div>

            {/* Center Chat Area */}
            <div className="flex-1 flex flex-col relative overflow-hidden bg-background">
                {children}
            </div>

            {/* Right Context Panel */}
            <div className="w-80 border-l bg-muted/10 flex flex-col">
                <div className="p-4 border-b font-medium text-sm flex items-center justify-between">
                    <span>Active Context</span>
                    <span className="flex h-2 w-2 rounded-full bg-green-500"></span>
                </div>
                <div className="flex-1 overflow-auto p-4">
                    {contextPanel}
                </div>
            </div>
        </div>
    );
}
