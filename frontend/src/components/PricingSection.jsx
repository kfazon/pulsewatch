import React from 'react';

const tiers = [
  {
    name: 'Starter',
    price: '$97',
    period: '/month',
    label: null,
    for: 'Solo consultants and new agencies getting serious about competitive positioning.',
    features: [
      '5 competitor profiles monitored',
      'Weekly intelligence digest (email)',
      'Basic market movement alerts',
      '1 user seat',
      'Community access (Slack)',
      'Email support (48-hour response)',
    ],
    cta: 'Start Starter',
    youGet: 'The foundational clarity to stop guessing what competitors are doing—and start acting on it.',
  },
  {
    name: 'Agency',
    price: '$297',
    period: '/month',
    label: 'Most Popular',
    for: 'Established agencies and consultancies who need deep, real-time competitive intelligence to protect and grow their pipeline.',
    features: [
      '20 competitor profiles monitored',
      'Real-time alerts (email + SMS)',
      'Daily intelligence briefings',
      'Advanced competitive positioning reports',
      '5 user seats',
      'Priority onboarding (live 1:1 setup call)',
      'Priority email + chat support',
      'Quarterly strategy review call',
      'White-label report templates',
    ],
    cta: 'Start Agency',
    youGet: 'The full intelligence operation to defend your accounts and acquire new ones—without hiring an in-house analyst.',
    featured: true,
  },
  {
    name: 'Enterprise',
    price: '$797',
    period: '/month',
    label: null,
    for: 'Larger agencies and firms with multi-market, multi-brand, or high-stakes competitive environments.',
    features: [
      'Unlimited competitor profiles',
      'Real-time alerts + dedicated webhook/API access',
      'Daily + weekly intelligence briefings (custom format)',
      'Executive-level competitive positioning reports',
      'Unlimited user seats',
      'Dedicated account manager',
      'White-glove onboarding + custom integrations',
      'Unlimited quarterly strategy reviews',
      'On-demand advisory calls (2x/month)',
      'Industry-specific intelligence add-ons available',
    ],
    cta: 'Contact Sales',
    youGet: 'Enterprise-grade intelligence with white-glove support—built for organizations where competitive blind spots cost real revenue.',
  },
];

export default function PricingSection() {
  return (
    <section style={{ padding: '80px 24px', background: '#fafafa', fontFamily: 'system-ui, sans-serif' }}>
      <h2 style={{ fontSize: '2rem', fontWeight: 700, textAlign: 'center', marginBottom: '8px' }}>Simple, Transparent Pricing</h2>
      <p style={{ textAlign: 'center', color: '#666', marginBottom: '48px' }}>
        One recovered account or newly won deal covers 3 months of Agency. Most clients see ROI within 60 days.
      </p>

      <div style={{ display: 'flex', gap: '24px', flexWrap: 'wrap', maxWidth: '1100px', margin: '0 auto' }}>
        {tiers.map((tier) => (
          <div
            key={tier.name}
            style={{
              flex: '1 1 280px',
              background: tier.featured ? '#111' : '#fff',
              color: tier.featured ? '#fff' : '#111',
              borderRadius: '12px',
              padding: '32px 24px',
              boxShadow: tier.featured ? '0 8px 32px rgba(0,0,0,0.15)' : '0 2px 8px rgba(0,0,0,0.06)',
              display: 'flex',
              flexDirection: 'column',
              position: 'relative',
            }}
          >
            {tier.label && (
              <span style={{
                position: 'absolute',
                top: '-12px',
                left: '50%',
                transform: 'translateX(-50%)',
                background: '#f59e0b',
                color: '#fff',
                fontSize: '0.75rem',
                fontWeight: 700,
                padding: '4px 12px',
                borderRadius: '20px',
              }}>
                {tier.label}
              </span>
            )}

            <h3 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '4px' }}>{tier.name}</h3>
            <div style={{ marginBottom: '8px' }}>
              <span style={{ fontSize: '2rem', fontWeight: 700 }}>{tier.price}</span>
              <span style={{ fontSize: '0.9rem', opacity: 0.7 }}>{tier.period}</span>
            </div>
            <p style={{ fontSize: '0.875rem', opacity: 0.8, marginBottom: '20px', lineHeight: 1.5 }}>{tier.for}</p>

            <ul style={{ listStyle: 'none', padding: 0, margin: '0 0 24px', flex: 1 }}>
              {tier.features.map((f) => (
                <li key={f} style={{ fontSize: '0.875rem', padding: '6px 0', borderBottom: `1px solid ${tier.featured ? 'rgba(255,255,255,0.1)' : '#eee'}`, display: 'flex', gap: '8px' }}>
                  <span style={{ color: tier.featured ? '#86efac' : '#22c55e' }}>✓</span>
                  {f}
                </li>
              ))}
            </ul>

            <p style={{ fontSize: '0.8rem', opacity: 0.7, marginBottom: '16px', fontStyle: 'italic' }}>You get: {tier.youGet}</p>

            <button style={{
              background: tier.featured ? '#fff' : '#111',
              color: tier.featured ? '#111' : '#fff',
              border: 'none',
              borderRadius: '6px',
              padding: '12px',
              fontWeight: 600,
              cursor: 'pointer',
              fontSize: '0.9rem',
            }}>
              {tier.cta}
            </button>
          </div>
        ))}
      </div>

      {/* Guarantee */}
      <div style={{ maxWidth: '600px', margin: '48px auto 0', textAlign: 'center' }}>
        <p style={{ fontSize: '0.9rem', color: '#666' }}>
          <strong>30-day money-back guarantee — no questions asked.</strong> If PulseWatch doesn't deliver actionable competitive intelligence within your first 30 days, we'll refund you in full. You keep any insights gathered.
        </p>
      </div>
    </section>
  );
}
