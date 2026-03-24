import React from 'react';

export default function LandingHero() {
  return (
    <section style={{ padding: '80px 24px', maxWidth: '800px', margin: '0 auto', fontFamily: 'system-ui, sans-serif' }}>
      {/* Headline */}
      <h1 style={{ fontSize: '2.5rem', fontWeight: 700, lineHeight: 1.2, marginBottom: '24px', color: '#111' }}>
        You're losing deals and you don't even know what your competitors just changed.
      </h1>

      {/* Subheadline */}
      <p style={{ fontSize: '1.25rem', lineHeight: 1.6, color: '#444', marginBottom: '40px' }}>
        PulseWatch gives agencies and consultants real-time intelligence on competitor positioning—so you can act before your prospects do. Stop guessing, start knowing.
      </p>

      {/* Problem Agitated */}
      <p style={{ fontSize: '1rem', lineHeight: 1.7, color: '#666', marginBottom: '40px', borderLeft: '3px solid #ddd', paddingLeft: '16px' }}>
        You've been posting consistently. You have a solid portfolio. But your close rate is slipping and you can't figure out why. Meanwhile, competitors you thought you'd left behind are suddenly winning the deals you wanted. The gap isn't your work—it's your visibility into what's actually shifting in your market.
      </p>

      {/* 3 Benefit Bullets */}
      <ul style={{ listStyle: 'none', padding: 0, marginBottom: '48px' }}>
        {[
          { label: 'Acquire', text: 'Get 25+ actionable competitor intelligence alerts per month—identify opportunities before your competition does and fill your pipeline with deals you actually want.' },
          { label: 'Defend', text: "Stop losing accounts without knowing why. When a prospect goes dark or a deal stalls, you'll know exactly what shifted and how to respond." },
          { label: 'Feel', text: 'Finally feel in control of your pipeline. Wake up knowing exactly which competitors are moving, what they\'re offering, and where your next opening is.' },
        ].map(({ label, text }) => (
          <li key={label} style={{ display: 'flex', gap: '12px', marginBottom: '16px', alignItems: 'flex-start' }}>
            <span style={{ fontWeight: 700, minWidth: '80px', color: '#111' }}>{label}:</span>
            <span style={{ color: '#333', lineHeight: 1.6 }}>{text}</span>
          </li>
        ))}
      </ul>

      {/* Social Proof */}
      <p style={{ fontSize: '1.1rem', fontWeight: 600, color: '#111', marginBottom: '8px' }}>
        Join 2,000+ agencies and independent consultants already monitoring their competitive landscape with PulseWatch.
      </p>
      <p style={{ fontSize: '0.875rem', color: '#888', marginBottom: '32px' }}>
        [Placeholder: Replace with verified count + 1–2 specific testimonials]
      </p>

      {/* FOMO CTA */}
      <div style={{ background: '#f5f5f5', borderRadius: '8px', padding: '24px', marginBottom: '24px' }}>
        <p style={{ fontSize: '1rem', fontWeight: 600, color: '#111', marginBottom: '8px' }}>
          Join the waitlist — only 20 founding-member spots open.
        </p>
        <p style={{ fontSize: '0.9rem', color: '#555', marginBottom: '16px' }}>
          Founding members lock in lifetime pricing and get priority onboarding. Once these 20 spots fill, the next pricing tier goes into effect.
        </p>
        <button style={{ background: '#111', color: '#fff', border: 'none', borderRadius: '6px', padding: '12px 24px', fontSize: '1rem', fontWeight: 600, cursor: 'pointer' }}>
          Join the Waitlist →
        </button>
      </div>

      {/* Risk Reversal */}
      <p style={{ fontSize: '0.9rem', color: '#666' }}>
        <strong>30-day money-back guarantee — no questions asked.</strong> If PulseWatch doesn't deliver actionable competitive intelligence within your first 30 days, we'll refund you in full. You can even keep the insights you gathered.
      </p>
    </section>
  );
}
