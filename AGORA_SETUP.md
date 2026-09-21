# Agora live panel: integration direction

Status: the current AI Panel is working turn-by-turn practice. Agora live audio
and talking video avatars are **not connected yet**. No Agora credentials are
configured locally, and no Agora SDK has been installed or billed session started.

## Proposed live flow

1. Candidate saves their role, experience, skills and projects in My Profile.
2. Flask creates an owner-scoped live session and issues short-lived channel tokens.
3. React joins an Agora RTC audio channel after the candidate starts the session.
4. The backend starts a Conversational AI agent with the confirmed profile and
   interviewer instructions. One persona speaks at a time; all share interview context.
5. Agora carries live audio, detects speech turns and handles interruptions. A
   managed ASR → LLM → TTS pipeline provides transcription, replies and speech.
6. The app records finalized conversation turns and persona handoffs. Partial
   transcripts must not be counted as completed answers.
7. Ending a session stops the cloud agent, closes the microphone and saves feedback.
   Disconnect and browser-close cleanup need testing before live mode is released.

Use managed voice models for the first integration to avoid requiring separate
ASR, LLM and TTS provider credentials. The exact models and voices will be selected
against the enabled Agora project. Keep the existing knowledge-assessment module
separate; live conversation feedback is coaching, not textbook-verified scoring.

## Local credentials needed

Create or select a project in [Agora Console](https://console.agora.io/), with
Conversational AI enabled. Keep these values in the project's local `.env` only:

```dotenv
AGORA_APP_ID=your_project_app_id
AGORA_APP_CERTIFICATE=your_project_app_certificate
```

Do not paste credentials into chat or frontend code. An App Certificate enables
server-side token authentication. Customer ID/secret are an alternative REST
authentication method, not an additional requirement when token authentication is used.
Provider-managed models can incur usage charges; check the project's current plan
before starting live sessions. Adding these variables alone does not activate live
mode: the RTC client, agent lifecycle, transcript handling and tests still need implementation.

## Voice versus video

Start with live voice and clear persona cards. Talking video avatars require an
additional avatar provider and integration; they are optional and not implied by
voice support. The user's voice/avatar preference is still pending.

## Official references checked September 20, 2026

- [Start and stop agents](https://docs.agora.io/en/ai/build/start-stop-agent)
- [Managed speech and language models](https://docs.agora.io/en/ai/build/custom-model-integration/managed-mode)
- [Server-side authentication](https://docs.agora.io/en/api-reference/api-ref/conversational-ai/authentication)
- [Live transcripts](https://docs.agora.io/en/ai/build/transcripts)
- [Conversational AI and avatar options](https://www.agora.io/en/products/conversational-ai-engine/)
