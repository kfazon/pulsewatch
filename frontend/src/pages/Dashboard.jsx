import React, { useState, useMemo } from 'react';
import { Link } from 'react-router-dom';

// ---------------------------------------------------------------------------
// Mock data – replace / augment with API calls to the backend in production
// ---------------------------------------------------------------------------
const MOCK_CAPTURES = [
  {
    id: 'c1',
    url: 'https://www.acme.com/pricing',
    capturedAt: '2026-03-24T15:33:59',
    category: 'pricing',
    importance: 0.92,
    summary:
      'Enterprise plan price increased from $99/mo to $129/mo. New "Growth" tier added at $79/mo. Annual discount changed from 20% to 15%.',
  },
  {
    id: 'c2',
    url: 'https://www.acme.com/features',
    capturedAt: '2026-03-24T14:12:01',
    category: 'product',
    importance: 0.65,
    summary:
      'Added new "AI-powered analytics" feature card. Screenshot comparison shows updated hero graphic. "Beta" badge removed from dark mode toggle.',
  },
  {
    id: 'c3',
    url: 'https://www.acme.com/contact',
    capturedAt: '2026-03-24T12:05:33',
    category: 'contact',
    importance: 0.31,
    summary:
      'Phone number updated from +1-800-555-0100 to +1-800-555-0199. Support email unchanged. Office address remains the same.',
  },
  {
    id: 'c4',
    url: 'https://www.acme.com/legal/terms',
    capturedAt: '2026-03-23T22:01:14',
    category: 'legal',
    importance: 0.88,
    summary:
      'Section 4.2 arbitration clause amended — opt-out window reduced from 30 days to 14 days. New data retention clause added (Section 7.4).',
  },
  {
    id: 'c5',
    url: 'https://www.acme.com/',
    capturedAt: '2026-03-23T18:44:02',
    category: 'product',
    importance: 0.44,
    summary:
      'Navigation bar reordered — "Pricing" moved from 3rd to 1st position. CTA button text changed from "Get Started" to "Start Free Trial".',
  },
  {
    id: 'c6',
    url: 'https://www.acme.com/changelog',
    capturedAt: '2026-03-23T09:30:00',
    category: 'other',
    importance: 0.18,
    summary:
      'Changelog entry added for v2.4.1 patch release — "Fixed intermittent login timeout on Safari". No content structural changes.',
  },
  {
    id: 'c7',
    url: 'https://www.acme.com/privacy',
    capturedAt: '2026-03-22T20:15:45',
    category: 'legal',
    importance: 0.95,
    summary:
      'Data sharing section rewritten — third-party广告 partners now explicitly named. New checkbox opt-in required for analytics cookies.',
  },
  {
    id: 'c8',
    url: 'https://www.acme.com/pricing',
    capturedAt: '2026-03-22T08:00:10',
    category: 'pricing',
    importance: 0.87,
    summary:
      'Free tier minutes reduced from 1000 to 500 per month. Overage pricing added: $0.004/min. Page layout refactored with new tier comparison table.',
  },
];

const CATEGORY_COLORS = {
  pricing: { bg: '#fee2e2', text: '#991b1b', border: '#fca5a5' },
  product: { bg: '#dbeafe', text: '#1e40af', border: '#93c5fd' },
  contact: { bg: '#dcfce7', text: '#166534', border: '#86efac' },
  legal: { bg: '#ffedd5', text: '#9a3412', border: '#fdba74' },
  other: { bg: '#f3f4f6', text: '#374151', border: '#d1d5db' },
};

function ImportanceBar({ value }) {
  const pct = Math.round(value * 100);
  const color =
    pct >= 75 ? '#ef4444' : pct >= 40 ? '#f59e0b' : '#22c55e';
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8, minWidth: 120 }}>
      <div
        style={{
          flex: 1,
          height: 6,
          background: '#e5e7eb',
          borderRadius: 3,
          overflow: 'hidden',
        }}
      >
        <div
          style={{
            width: `${pct}%`,
            height: '100%',
            background: color,
            borderRadius: 3,
            transition: 'width 0.3s',
          }}
        />
      </div>
      <span style={{ fontSize: 12, color: '#6b7280', minWidth: 32, textAlign: 'right' }}>
        {pct}%
      </span>
    </div>
  );
}

function CategoryBadge({ category }) {
  const colors = CATEGORY_COLORS[category] || CATEGORY_COLORS.other;
  return (
    <span
      style={{
        display: 'inline-block',
        padding: '2px 8px',
        borderRadius: 9999,
        fontSize: 11,
        fontWeight: 600,
        letterSpacing: '0.03em',
        textTransform: 'uppercase',
        background: colors.bg,
        color: colors.text,
        border: `1px solid ${colors.border}`,
      }}
    >
      {category}
    </span>
  );
}

function formatRelativeTime(isoString) {
  const now = new Date('2026-03-24T17:00:00');
  const then = new Date(isoString);
  const diffMs = now - then;
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  return `${diffDays}d ago`;
}

function formatTimestamp(isoString) {
  return new Date(isoString).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

// ---------------------------------------------------------------------------
// Dashboard page
// ---------------------------------------------------------------------------
export default function Dashboard() {
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('all');
  const [minImportance, setMinImportance] = useState(0);

  const filtered = useMemo(() => {
    return MOCK_CAPTURES.filter((c) => {
      const matchesSearch =
        !search || c.url.toLowerCase().includes(search.toLowerCase()) || c.summary.toLowerCase().includes(search.toLowerCase());
      const matchesCategory = category === 'all' || c.category === category;
      const matchesImportance = c.importance >= minImportance / 100;
      return matchesSearch && matchesCategory && matchesImportance;
    });
  }, [search, category, minImportance]);

  return (
    <div style={{ minHeight: '100vh', background: '#f9fafb', fontFamily: 'system-ui, sans-serif' }}>
      {/* Header */}
      <header
        style={{
          background: '#111827',
          color: '#fff',
          padding: '16px 24px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <div>
          <h1 style={{ fontSize: 18, fontWeight: 700, margin: 0 }}>
            PulseWatch
            <span style={{ fontWeight: 400, color: '#9ca3af', marginLeft: 8, fontSize: 13 }}>
              Internal Dashboard
            </span>
          </h1>
          <p style={{ fontSize: 12, color: '#6b7280', margin: '2px 0 0' }}>
            {MOCK_CAPTURES.length} targets monitored · {filtered.length} captures shown
          </p>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span
            style={{
              width: 8,
              height: 8,
              borderRadius: '50%',
              background: '#22c55e',
              display: 'inline-block',
            }}
          />
          <span style={{ fontSize: 12, color: '#9ca3af' }}>Live feed</span>
        </div>
      </header>

      <div style={{ maxWidth: 1100, margin: '0 auto', padding: '24px' }}>
        {/* Filters */}
        <div
          style={{
            background: '#fff',
            border: '1px solid #e5e7eb',
            borderRadius: 8,
            padding: 16,
            marginBottom: 16,
            display: 'flex',
            flexWrap: 'wrap',
            gap: 12,
            alignItems: 'center',
          }}
        >
          {/* Search */}
          <div style={{ flex: '1 1 240px' }}>
            <label style={{ fontSize: 11, fontWeight: 600, color: '#6b7280', textTransform: 'uppercase', display: 'block', marginBottom: 4 }}>
              Search
            </label>
            <input
              type="text"
              placeholder="URL or summary keyword…"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              style={{
                width: '100%',
                boxSizing: 'border-box',
                padding: '6px 10px',
                border: '1px solid #d1d5db',
                borderRadius: 6,
                fontSize: 13,
                outline: 'none',
              }}
            />
          </div>

          {/* Category filter */}
          <div style={{ flex: '0 0 160px' }}>
            <label style={{ fontSize: 11, fontWeight: 600, color: '#6b7280', textTransform: 'uppercase', display: 'block', marginBottom: 4 }}>
              Category
            </label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              style={{
                width: '100%',
                padding: '6px 10px',
                border: '1px solid #d1d5db',
                borderRadius: 6,
                fontSize: 13,
                background: '#fff',
                outline: 'none',
              }}
            >
              <option value="all">All categories</option>
              <option value="pricing">Pricing</option>
              <option value="product">Product</option>
              <option value="contact">Contact</option>
              <option value="legal">Legal</option>
              <option value="other">Other</option>
            </select>
          </div>

          {/* Importance threshold */}
          <div style={{ flex: '0 0 200px' }}>
            <label style={{ fontSize: 11, fontWeight: 600, color: '#6b7280', textTransform: 'uppercase', display: 'block', marginBottom: 4 }}>
              Min Importance: <span style={{ color: '#111827' }}>{minImportance}%</span>
            </label>
            <input
              type="range"
              min="0"
              max="100"
              step="5"
              value={minImportance}
              onChange={(e) => setMinImportance(Number(e.target.value))}
              style={{ width: '100%', accentColor: '#3b82f6' }}
            />
          </div>
        </div>

        {/* Capture feed */}
        {filtered.length === 0 ? (
          <div
            style={{
              textAlign: 'center',
              padding: '48px 24px',
              color: '#6b7280',
              background: '#fff',
              border: '1px solid #e5e7eb',
              borderRadius: 8,
            }}
          >
            No captures match the current filters.
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {filtered.map((capture) => (
              <Link
                key={capture.id}
                to={`/capture/${capture.id}`}
                style={{ textDecoration: 'none' }}
              >
                <div
                  style={{
                    background: '#fff',
                    border: '1px solid #e5e7eb',
                    borderRadius: 8,
                    padding: '14px 16px',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: 8,
                    cursor: 'pointer',
                    transition: 'box-shadow 0.15s, border-color 0.15s',
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.boxShadow = '0 2px 8px rgba(0,0,0,0.08)';
                    e.currentTarget.style.borderColor = '#9ca3af';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.boxShadow = 'none';
                    e.currentTarget.style.borderColor = '#e5e7eb';
                  }}
                >
                  {/* Top row */}
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 8 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 10, minWidth: 0 }}>
                      <CategoryBadge category={capture.category} />
                      <span
                        style={{
                          fontSize: 13,
                          fontFamily: 'monospace',
                          color: '#374151',
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          whiteSpace: 'nowrap',
                          maxWidth: 400,
                        }}
                        title={capture.url}
                      >
                        {capture.url}
                      </span>
                    </div>
                    <span style={{ fontSize: 12, color: '#9ca3af', whiteSpace: 'nowrap' }}>
                      {formatRelativeTime(capture.capturedAt)} · {formatTimestamp(capture.capturedAt)}
                    </span>
                  </div>

                  {/* Summary */}
                  <p
                    style={{
                      fontSize: 13,
                      color: '#4b5563',
                      margin: 0,
                      lineHeight: 1.5,
                      display: '-webkit-box',
                      WebkitLineClamp: 2,
                      WebkitBoxOrient: 'vertical',
                      overflow: 'hidden',
                    }}
                  >
                    {capture.summary}
                  </p>

                  {/* Importance bar */}
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <span style={{ fontSize: 11, color: '#6b7280', minWidth: 80 }}>Importance</span>
                    <ImportanceBar value={capture.importance} />
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
