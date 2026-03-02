# Affiliate AI Pro — Deployed System

## Live URLs
- Frontend: https://affiliate-ai-frontend.vercel.app
- Backend: https://affiliate-ai-backend.onrender.com
- Health: https://affiliate-ai-backend.onrender.com/api/health

## Features
- Multi-platform affiliate marketing (Instagram, Facebook, TikTok, YouTube, LinkedIn)
- AI Executive Assistant with persona switching
- Executive Autopilot (learns your habits)
- Dead Man’s Switch (auto-engage if inactive)
- Rules Engine (pre-set campaigns/payouts)
- GitHub Actions cron (runs every 6 hours)
- TOTP 2FA
- Payouts (PayPal, Cash App, Chime, Bank, Crypto)
- Device session management
- Security hardening (rate limiting, audit logging, SMS alerts)

## How to Use
1) Register/login at the frontend URL
2) Create campaigns per platform
3) Use AI Chat for marketing commands
4) Configure 2FA and Dead Man’s Switch
5) Add Rules for offline automation
6) Set up payouts

## Offline/Autonomous Operation
- GitHub Actions calls `/api/scheduler/run` every 6 hours
- Scheduler evaluates rules, runs autopilot, checks dead man’s switch
- Your AI assistants keep launching campaigns and requesting payouts

## Security
- All actions are audited
- Rate limiting and suspicious request detection
- Optional SMS alerts
- 2FA support

## Environment Variables (Render)
- `SCHEDULER_TOKEN=AiPro2026SchedulerToken9f8k3d2s1`
- Add other keys (Supabase, Twilio, Google) as needed

## GitHub Secrets
- `SCHEDULER_TOKEN=AiPro2026SchedulerToken9f8k3d2s1`

## Support
- Check `/api/health` for service status
- Review logs in Render dashboard
- Check GitHub Actions workflow runs

Your system is fully autonomous and will keep earning money even if you’re offline.
