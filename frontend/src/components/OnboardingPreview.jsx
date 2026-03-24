import React from 'react';

const steps = [
  { day: 'Day 0', title: 'Welcome', desc: 'Connect your CRM, website, and key markets in under 10 minutes. No developer required.' },
  { day: 'Day 1', title: 'Quick Win', desc: 'Add your top 3 most-worrisome competitors and run your first basic movement scan.' },
  { day: 'Day 3', title: 'Setup Reminder', desc: 'Add your top 5 competitors, turn on real-time alerts, and set your first Monday briefing.' },
  { day: 'Day 7', title: 'First Insight', desc: 'Receive your first plain-English intelligence brief on what competitors changed this week.' },
  { day: 'Day 14', title: 'Landscape Report', desc: 'Get your 2-week competitive landscape report showing every significant move.' },
  { day: 'Day 21', title: 'Upgrade Prompt', desc: 'Discover if Starter or Agency is the right fit for your competitive intelligence needs.' },
  { day: 'Day 30', title: 'Renewal', desc: 'Lock in your next 30 days with a full intelligence operation behind you.' },
];

export default function OnboardingPreview() {
  return (
    <section style={{ padding: '80px 24px', maxWidth: '900px', margin: '0 auto', fontFamily: 'system-ui, sans-serif' }}>
      <h2 style={{ fontSize: '2rem', fontWeight: 700, marginBottom: '8px' }}>Up and Running in 10 Minutes</h2>
      <p style={{ color: '#666', marginBottom: '48px' }}>
        Here's the 3-step process to start receiving competitive intelligence.
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: '24px' }}>
        {steps.map((step, i) => (
          <div key={step.day} style={{ display: 'flex', gap: '16px', alignItems: 'flex-start' }}>
            <div style={{
              minWidth: '36px',
              height: '36px',
              borderRadius: '50%',
              background: '#111',
              color: '#fff',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: 700,
              fontSize: '0.8rem',
              flexShrink: 0,
            }}>
              {i + 1}
            </div>
            <div>
              <div style={{ fontSize: '0.75rem', fontWeight: 600, color: '#888', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '2px' }}>
                {step.day}
              </div>
              <div style={{ fontWeight: 700, marginBottom: '4px' }}>{step.title}</div>
              <div style={{ fontSize: '0.875rem', color: '#555', lineHeight: 1.5 }}>{step.desc}</div>
            </div>
          </div>
        ))}
      </div>

      {/* 3-Step Summary */}
      <div style={{ marginTop: '48px', background: '#f5f5f5', borderRadius: '8px', padding: '24px' }}>
        <h3 style={{ fontWeight: 700, marginBottom: '16px' }}>The 3-Step Setup</h3>
        <ol style={{ paddingLeft: '20px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <li><strong>Connect your tools</strong> — Link your CRM, website, and key markets in under 10 minutes. No developer required.</li>
          <li><strong>Define your watch list</strong> — Tell us which competitors matter most to your business. We'll build your custom monitoring dashboard.</li>
          <li><strong>Receive weekly intelligence briefs</strong> — Every Monday morning, get a plain-English breakdown of what your competitors changed, what it means for you, and what to do next.</li>
        </ol>
      </div>
    </section>
  );
}
