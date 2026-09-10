import { useEffect, useMemo, useRef, useState } from "react";
import { useLocation, useParams } from "react-router-dom";
import {
  AssistantRuntimeProvider,
  useLocalRuntime,
} from "@assistant-ui/react";
import { getTripById, sendChatMessage } from "../api/api";
import { Thread } from "../components/assistant-ui/thread.aui";

function formatItinerary(itinerary = []) {
  return itinerary
    .map((day) => {
      const places = (day.places ?? [])
        .map((place) => {
          const type = place.type === "food" ? "food" : "sight";
          return `- ${type}: ${place.name}`;
        })
        .join("\n");

      return `### Day ${day.day}\n${places}`;
    })
    .join("\n\n");
}


function ConversationContent() {
  const { tripId } = useParams();
  const { state } = useLocation();
  const [plan, setPlan] = useState(tripId ? null : state);

  useEffect(() => {
    if (!tripId) {
      return;
    }

    getTripById(tripId).then((response) => {
      setPlan({
        ...response.data,
        tripId: response.data.id,
      });
    });
  }, [tripId]);

  if (!plan) {
    return <p>Loading conversation...</p>;
  }

  return <ConversationThread plan={plan} />;
}

function ConversationThread({ plan }) {
  const itineraryRef = useRef(plan.itinerary ?? []);

  const initialMessages = useMemo(
    () =>
      (plan.messages ?? []).map((message, index, messages) => ({
        id: String(message.id),
        role: message.role,
        content:
          index === messages.length - 1 && message.role === "assistant"
            ? `${message.content}\n\n${formatItinerary(plan.itinerary ?? [])}`
            : message.content,
      })),
    [plan.messages, plan.itinerary],
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

      const response = await sendChatMessage({
        message,
        city: plan.city,
        days: plan.days,
        current_itinerary: itineraryRef.current,
        trip_id: plan.tripId ?? plan.id ?? null,
      });

      itineraryRef.current = response.itinerary;

      return {
  content: [
    {
      type: "text",
      text: `${response.assistant_reply}\n\n${formatItinerary(
        response.itinerary ?? [],
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