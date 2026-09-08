import { useMemo, useRef } from "react";
import { useLocation } from "react-router-dom";
import {
  AssistantRuntimeProvider,
  useLocalRuntime,
} from "@assistant-ui/react";
import { sendChatMessage } from "../api/api";
import { Thread } from "../components/assistant-ui/thread.aui";

function formatItinerary(itinerary) {
  return itinerary
    .map((day) => {
      const places = day.places
        .map((place) => {
          const type = place.type === "food" ? "food" : "sight";
          return `- ${type}：${place.name}`;
        })
        .join("\n");

      return `### Day ${day.day} \n${places}`;
    })
    .join("\n\n");
}


function ConversationContent() {
  const { state } = useLocation();

  const plan = state ?? {
    city: "",
    days: 1,
    itinerary: [],
    tripId: null,
  };

  const itineraryRef = useRef(plan.itinerary);

  const initialMessages = useMemo(
  () => [
    {
      id: "initial-user-message",
      role: "user",
      content: `Generate a ${plan.city} ${plan.days} day travel plan.`,
    },
    {
      id: "initial-assistant-message",
      role: "assistant",
      content: `Good, here is the ${plan.city} ${plan.days} day travel plan generated for you:\n\n${formatItinerary(
        plan.itinerary,
      )}`,
    },
  ],
  [plan.city, plan.days, plan.itinerary],
);

  const chatModel = {
    async run({ messages }) {
      const latestUserMessage = [...messages]
        .reverse()
        .find((message) => message.role === "user");

      const message =
        latestUserMessage?.content
          ?.filter((part) => part.type === "text")
          .map((part) => part.text)
          .join("") ?? "";

      const history = messages.map((item) => ({
        role: item.role,
        content:
          item.content
            ?.filter((part) => part.type === "text")
            .map((part) => part.text)
            .join("") ?? "",
      }));

      const response = await sendChatMessage({
        message,
        history,
        city: plan.city,
        days: plan.days,
        current_itinerary: itineraryRef.current,
        trip_id: plan.tripId,
      });

      itineraryRef.current = response.itinerary;

      return {
        content: [
          {
            type: "text",
            text: `${response.assistant_reply}\n\n${formatItinerary(
              response.itinerary,
            )}`,
          },
        ],
      };
    },
  };

  const runtime = useLocalRuntime(chatModel, {
    initialMessages,
  });

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <Thread />
    </AssistantRuntimeProvider>
  );
}

export default function ConversationPage() {
  return (
    <div className="h-[calc(100vh-64px)]">
      <ConversationContent />
    </div>
  );
}