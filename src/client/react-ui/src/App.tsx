import { MainLayout } from "@/components/layout/MainLayout";
import { ChatWindow } from "@/components/chat/ChatWindow";
import { ChatInput } from "@/components/chat/ChatInput";
import { useAgentChat } from "@/hooks/useAgentChat";
import { Badge } from "@/components/ui/badge";

function App() {
  const { messages, isTyping, sessionContext, sendMessage, approveAction, rejectAction } = useAgentChat();

  const contextPanel = (
    <div className="space-y-4">
      <div className="mb-4">
        <h3 className="font-semibold text-sm mb-1 text-primary">Live Data Feed</h3>
        <p className="text-xs text-muted-foreground">Synchronized with C# Desktop Bridge</p>
      </div>

      <div className="bg-background rounded-lg border p-3 shadow-sm">
        <div className="flex justify-between items-center mb-2">
          <span className="text-xs font-semibold text-muted-foreground uppercase">Target Context</span>
        </div>
        <div className="space-y-2 text-sm font-mono bg-muted/30 p-2 rounded max-h-48 overflow-auto break-all">
          <pre className="text-xs">{JSON.stringify(sessionContext, null, 2)}</pre>
        </div>
        <div className="mt-3 flex gap-2">
          <Badge variant="outline" className="border-green-500/30 text-green-700 bg-green-500/10">Connected</Badge>
          <Badge variant="secondary" className="font-mono">{sessionContext.selected_item}</Badge>
        </div>
      </div>
    </div>
  );

  return (
    <MainLayout contextPanel={contextPanel}>
      <ChatWindow
        messages={messages}
        isTyping={isTyping}
        onApproveAction={approveAction}
        onRejectAction={rejectAction}
      />
      <div className="mt-auto">
        <ChatInput onSendMessage={sendMessage} disabled={isTyping} />
      </div>
    </MainLayout>
  );
}

export default App;
