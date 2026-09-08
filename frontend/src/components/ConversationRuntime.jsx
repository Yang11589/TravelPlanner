import {
  AssistantRuntimeProvider,
  useLocalRuntime,
} from "@assistant-ui/react";
import { sendChatMessage } from "../api/api";
import { Thread } from "../components/assistant-ui/thread.aui";

function ConversationRuntimeInner() {
  const chatModel = {
    async run({ messages }) {
      const history = messages.map((message) => ({
        role: message.role,
        content: message.content
          .filter((part) => part.type === "text")
          .map((part) => part.text)
          .join(""),
      }));

      const latestMessage = [...messages]
        .reverse()
        .find((message) => message.role === "user");

      const message = latestMessage?.content
        ?.filter((part) => part.type === "text")
        .map((part) => part.text)
        .join("") || "";

      const response = await sendChatMessage({
        message,
        history,
        city: "Paris",
        days: 3,
        current_itinerary: [],
      });

      return {
        content: [
          {
            type: "text",
            text: response.assistant_reply,
          },
        ],
      };
    },
  };

  const runtime = useLocalRuntime(chatModel);

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <Thread />
    </AssistantRuntimeProvider>
  );
}

export default ConversationRuntimeInner;