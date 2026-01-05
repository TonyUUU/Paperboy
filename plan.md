# Paperboy Design Plan

## Role
- Agent: search online for news, learn from feedback
  - learn from feedback
  - fetch news
- System: format news, send to notion, store feedback in memory
  - send instruction to agent to fetch news
  - format news into daily paper
  - send paper to notion
  - receive feedback from notion webhook
  - store feedback in memory
- Notion: database for news and feedback
  - display news
  - collect feedback from user
  - send feedback to system via webhook
- User: provide feedback on news

## Workflow
1. **System** sends instruction to agent to fetch news
2. **Agent** fetches news and sends back to system
3. **System** formats news into daily paper
4. **System** sends paper to notion database
5. **User** views news in notion and provides feedback
6. **Notion** sends feedback to system via webhook
7. **System** stores feedback in memory for agent to learn
8. **Agent** learns from feedback in memory

## Technology Stack
- Agent model: Google Gemini
- Backend: Python fastAPI
- Database: Turso Libsql
- Frontend: Notion
- Host: Google Cloud Run
- Scheduling: Google Cloud Scheduler
- CI/CD: GitHub Actions

## Misc
- notion_client: a python client to interact with notion database
- notion webhook: to receive feedback from notion (need to host an endpoint to receive webhook)
- memory: a simple database to store feedback for agent to learn (sqlite with vector support and langgraph memory)
- user feedback: like or dislike to a certain news article

- backend component: python system, sqlite database -- consider containerize with docker
- frontend component: notion database -- no need to host, use notion service
- agent model: Google Gemini
- db consideration: can use Turso for free small db hosting

## Memo
- deploy one image for two purpose (service + job)
  - service: receive webhook from notion
  - job: scheduled job to fetch news and send to notion
