import ChatBox from "../components/ChatBox"

export default function ChatPage() {
  return (
    <div className="min-h-screen bg-background selection:bg-primary/20">
      <main className="pt-24">
        <ChatBox />
      </main>
    </div>
  )
}