"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Loader2, Sparkles } from "lucide-react";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  suggestions?: string[];
}

const SUGGESTED_ACTIONS = [
  "What items can I rent nearby?",
  "How can I earn from my home?",
  "Find me a power drill",
  "What storage options are available?",
  "Show me local delivery services",
  "Help me list an item",
];

const getApiUrl = () => {
  if (typeof window !== "undefined") {
    // On client side, use relative URLs or detect from environment
    return process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  }
  return "http://localhost:8000";
};

export function ModernChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      content:
        "Hi! I'm MEMBRA, a marketplace you talk to. Ask me what you need nearby, what you can earn from your home, or get local recommendations. What can I help you with today?",
      timestamp: new Date(),
      suggestions: SUGGESTED_ACTIONS.slice(0, 3),
    },
  ]);

  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [streamingContent, setStreamingContent] = useState("");
  const [apiUrl, setApiUrl] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setApiUrl(getApiUrl());
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, streamingContent]);

  const handleSendMessage = async (messageText?: string) => {
    const text = messageText || input.trim();
    if (!text) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: text,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);
    setStreamingContent("");

    try {
      const response = await fetch(`${apiUrl}/api/v1/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: "user_123",
          message: text,
        }),
      });

      if (!response.ok) throw new Error("Failed to send message");

      const reader = response.body?.getReader();
      if (!reader) throw new Error("No readable stream");

      const decoder = new TextDecoder();
      let content = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        content += chunk;
        setStreamingContent(content);
      }

      // Parse streaming response - extract suggestions if present
      let fullResponse = content;
      let suggestions = [];

      // Try to extract JSON suggestions from the end
      const jsonMatch = content.match(/\[[\s\S]*\]$/);
      if (jsonMatch) {
        try {
          suggestions = JSON.parse(jsonMatch[0]);
          fullResponse = content.substring(0, jsonMatch.index).trim();
        } catch (e) {
          // If JSON parsing fails, treat entire content as response
        }
      }

      // Add assistant message
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: fullResponse || content,
        timestamp: new Date(),
        suggestions: suggestions.length > 0 ? suggestions : undefined,
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setStreamingContent("");
    } catch (error) {
      console.error("Chat error:", error);

      // Fallback response
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content:
          "I'm having trouble connecting. Please try again. You can ask me to find items nearby, show earning opportunities, or help with marketplace needs.",
        timestamp: new Date(),
        suggestions: SUGGESTED_ACTIONS.slice(0, 3),
      };

      setMessages((prev) => [...prev, errorMessage]);
      setStreamingContent("");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-b from-black via-gray-950 to-black">
      {/* Header */}
      <div className="border-b border-amber-500/10 bg-black/50 backdrop-blur px-6 py-4">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <Sparkles className="w-5 h-5 text-amber-400" />
          <div>
            <h1 className="text-xl font-bold text-white">MEMBRA Assistant</h1>
            <p className="text-xs text-gray-400">
              A marketplace you talk to
            </p>
          </div>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto px-6 py-8 space-y-6">
          {messages.map((message) => (
            <div key={message.id} className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}>
              <div
                className={`max-w-2xl rounded-2xl px-6 py-4 ${
                  message.role === "user"
                    ? "bg-amber-500/20 border border-amber-500/30 text-white"
                    : "bg-gray-900/50 border border-amber-500/10 text-gray-100"
                }`}
              >
                <p className="text-sm leading-relaxed whitespace-pre-wrap">
                  {message.content}
                </p>

                {/* Suggestions */}
                {message.role === "assistant" && message.suggestions && message.suggestions.length > 0 && (
                  <div className="mt-4 pt-4 border-t border-amber-500/10 space-y-2">
                    <p className="text-xs font-semibold text-amber-400/70 uppercase tracking-wider">
                      Try asking:
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {message.suggestions.map((suggestion, idx) => (
                        <button
                          key={idx}
                          onClick={() => handleSendMessage(suggestion)}
                          className="text-xs bg-amber-500/10 border border-amber-500/30 text-amber-200 px-3 py-2 rounded-lg hover:bg-amber-500/20 transition-all duration-200"
                        >
                          {suggestion}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}

          {/* Streaming Response */}
          {streamingContent && (
            <div className="flex justify-start">
              <div className="max-w-2xl rounded-2xl px-6 py-4 bg-gray-900/50 border border-amber-500/10 text-gray-100 animate-pulse">
                <p className="text-sm leading-relaxed whitespace-pre-wrap">
                  {streamingContent}
                </p>
              </div>
            </div>
          )}

          {/* Loading Indicator */}
          {isLoading && !streamingContent && (
            <div className="flex justify-start">
              <div className="bg-gray-900/50 border border-amber-500/10 rounded-2xl px-6 py-4">
                <div className="flex gap-2 items-center text-gray-400">
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span className="text-sm">MEMBRA is thinking...</span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="border-t border-amber-500/10 bg-black/50 backdrop-blur px-6 py-6">
        <div className="max-w-4xl mx-auto">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage();
            }}
            className="flex gap-3"
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask MEMBRA anything nearby..."
              disabled={isLoading}
              className="flex-1 bg-gray-900/50 border border-amber-500/20 rounded-2xl px-6 py-4 text-white placeholder:text-gray-500 focus:outline-none focus:border-amber-500/50 focus:ring-1 focus:ring-amber-500/20 transition-all disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="bg-amber-400 hover:bg-amber-300 disabled:opacity-50 disabled:cursor-not-allowed text-black font-bold rounded-2xl px-6 py-4 transition-all flex items-center gap-2 whiteespace-nowrap"
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Send className="w-4 h-4" />
              )}
              <span className="hidden sm:inline">Send</span>
            </button>
          </form>

          {/* Quick Actions */}
          {messages.length === 1 && (
            <div className="mt-4 space-y-2">
              <p className="text-xs font-semibold text-amber-400/70 uppercase tracking-wider">
                Quick start:
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {SUGGESTED_ACTIONS.slice(0, 4).map((action, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSendMessage(action)}
                    className="text-xs bg-gray-900/50 border border-amber-500/20 text-gray-300 px-4 py-3 rounded-xl hover:border-amber-500/50 hover:bg-gray-900/70 transition-all text-left"
                  >
                    {action}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
