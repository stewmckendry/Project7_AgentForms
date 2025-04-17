# 🧠 Updated End-to-End Flow: Concussion Assistant App

## 🎯 Core Goals
1. **“Does my child have a concussion?”**  
   → Conversational assessment based on symptoms, activities, risks  
2. **“Can my child play [sport/activity]?”**  
   → Interactive protocol lookup + return-to-play (RTP) stage guidance  

---

## 🧭 App Flow Overview

```
      ┌──────────────────────────────┐
      │     App Landing (Welcome)    │
      └────────────┬─────────────────┘
                   ▼
     ┌──────────────────────────────┐
     │ Ask: “How can I help today?” │
     │ a) Assess possible concussion│
     │ b) Ask about return-to-play  │
     └────────────┬─────────────────┘
                  │
 ┌────────────────▼─────────────────────┐
 │ A. Concussion Assessment Path        │
 └────────────────┬─────────────────────┘
                  ▼
     1. Free-form situation input
     2. LLM drafts responses to assessment questions
     3. LLM interpreters parse: dates, symptoms, yes/no, etc.
     4. LLM generates follow-up questions based on uncertainty or risk
     5. Finalize structured responses
     6. Generate personalized guidance (summary + protocol-based recommendations)

 ┌────────────────▼─────────────────────┐
 │ B. Return-to-Play (RTP) Q&A Path     │
 └────────────────┬─────────────────────┘
                  ▼
     1. Ask: “What activity are you wondering about?”
     2. Check current symptom/resolution status (optional or use assessment data if available)
     3. Search `return_to_play.yaml` for:
         - Is activity allowed in any stage?
         - What’s the stage's name, description, and progression rules?
         - Risks if done too early
     4. Respond with protocol-based advice (plus reminder it’s not a medical diagnosis)

 ┌────────────────▼─────────────────────┐
 │ Optional: Combine Paths              │
 └────────────────┬─────────────────────┘
                  ▼
     After assessment, user may ask:
     👉 “Can they skate yet?” or “Are we ready for a game?”
     ➤ App uses current inferred RTP stage to answer questions about specific activities
```