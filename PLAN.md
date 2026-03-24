# PulseWatch Go-to-Market Plan v1.0

## Competitive Analysis

### Direct Competitors

| Tool | Price | Key Features | Weakness |
|------|-------|--------------|----------|
| **Visualping** | ~$15-80/mo | 2M+ users, Fortune 500, AI importance scoring | Expensive, generic, not Discord-native |
| **changedetection.io** | $8.99/mo | 5000 URLs, open source, 85+ integrations | No AI summaries on basic, commodity product |
| **PageCrawl.io** | ~$20-80/mo | AI summaries (enterprise only), price monitoring | Expensive for AI, complex |
| **UptimeRobot** | Free tier | Change detection + uptime, free | Not AI-powered, generic |
| **Prisync/Price2Spy** | ~$50-200/mo | E-commerce price focused | Too narrow, not general competitor intel |

### Market Positioning

**Tržište:** Website change detection je commoditizirano, ali AI-powered competitor intelligence je still nascent.

**Trend:** 
- Basic monitoring (changedetection) → $8.99/mo, low margin
- AI summaries (Visualping, PageCrawl) → $15-80/mo, premium
- Discord-native delivery → expectation, not differentiator

### PulseWatch's Differentiation

**Current state (from repo):**
- Playwright scraping + screenshots
- DOM + screenshot diffing  
- LLM summarization with importance scoring
- Discord delivery (daily/weekly digest)

**Differentiated positioning:**
1. **AI-native**: LLM summaries built-in, not enterprise-upsell
2. **Discord-first**: Built for Discord from day 1, not email-with-Discord-option
3. **Digest format**: Daily/weekly intel instead of noisy real-time alerts
4. **Competitor focus**: Not "monitor any page" — specifically for competitive intelligence

---

## Target Audience

### Primary Buyer Persona: "Growth Detective"

**Who:** Product Growth Manager / Competitive Intelligence Lead  
**Company:** Series A-B SaaS, 20-200 employees  
**Team:** Growth, Product, Marketing  
**Tools they use:** Discord, Notion, Slack  
**Pain:** "I spend 2h/day checking competitor websites and still miss things"

### Secondary: Agency Teams

**Who:** Account Manager / Strategist  
**Company:** Digital marketing/consulting agency  
**Monitoring:** 10-50 competitor sites for multiple clients  
**Pain:** "Need to alert clients fast when competitors move"

### Tertiary: Product Teams

**Who:** Product Manager  
**Need:** Track competitor feature releases, pricing changes  
**Pain:** "Missed that competitor launched X feature until our sales team told us"

---

## Pain Points (from market research)

1. **Noise problem**: Existing tools send "page changed" alerts, not "this matters"
2. **Manual effort**: Have to check multiple sources to understand context
3. **Slow reaction**: By the time they notice, competitor already gained advantage
4. **No prioritization**: All changes treated equally, important stuff buried

---

## Value Proposition

**Headline:** "Never Miss When Your Competitors Move"

**Subheadline:** "AI-powered competitor monitoring that tells you what changed AND why it matters — delivered to Discord before your team hears it from someone else."

**3 Key Benefits:**
1. **AI Intelligence** — Summarizes changes and scores importance so you see what matters
2. **Zero Noise** — Digest delivery instead of endless notifications
3. **Team-Ready** — Discord-native, built for how growth teams actually work

---

## Pricing Strategy

### Competitor Benchmarks
- Basic change detection: $8.99-15/mo
- AI-powered: $15-80/mo
- Enterprise: $80-200/mo

### PulseWatch MVP Pricing

| Tier | Price | Limits | Target |
|------|-------|--------|--------|
| **Free** | $0 | 3 URLs, daily digest | Trial users, indie hackers |
| **Pro** | $19/mo | 20 URLs, hourly + digest | Growth teams, small agencies |
| **Agency** | $49/mo | 100 URLs, multiple teams | Agencies with multiple clients |

**Note:** Start with Free + Pro only. Agency tier later.

---

## Go-to-Market Phases

### Phase 1: MVP Launch (Weeks 1-2)
- Landing page live ✅
- Waitlist collection
- Discord webhook notification
- Focus: Collect emails, validate interest

### Phase 2: Early Adopters (Weeks 3-4)
- Manual onboarding of first 10-20 users
- Discord community
- Gather feedback
- Focus: Product-market fit validation

### Phase 3: Public Beta (Weeks 5-8)
- Free tier open to public
- Launch on Product Hunt
- Outreach to target communities (Indie Hackers, Hacker News)
- Focus: User acquisition

### Phase 4: Paid Launch (Weeks 9-12)
- Stripe integration
- Pro tier available
- Case studies from early users
- Focus: Revenue

---

## Channels & Tactics

### Organic (Primary)
1. **Product Hunt** launch
2. **Hacker News** "Show HN" post
3. **Indie Hackers** case study/interview
4. **Twitter/X** thread on "how we built PulseWatch"
5. **Reddit** r/SideProject, r/startups, r/SaaS

### Community (Secondary)
1. **Discord servers** for startups/growth/ SaaS communities
2. **LinkedIn** posts targeting growth/product roles

### Content (Tertiary)
1. Blog post: "How to monitor competitors without spending hours"
2. Twitter thread: "Signs your competitor is about to make a move"

---

## Success Metrics

| Metric | Week 2 | Week 4 | Week 8 | Week 12 |
|--------|--------|--------|--------|---------|
| Waitlist signups | 100 | 500 | 2000 | 5000 |
| Discord community | - | 50 | 200 | 500 |
| Active users (free) | - | 20 | 100 | 500 |
| Paying users | - | - | 5 | 50 |
| MRR | - | - | $100 | $1,000 |

---

## Immediate Actions (This Week)

1. [x] Landing page deployed
2. [ ] Update landing page copy with correct positioning
3. [ ] Add waitlist counter ("Join X others")
4. [ ] Set up Stripe (for future payments)
5. [ ] Create Discord community server
6. [ ] Post waitlist link to social channels

---

## Files

- Landing page: `/home/pulsewatch/public_html/index.html`
- Subscribe handler: `/home/pulsewatch/public_html/subscribe.php`
