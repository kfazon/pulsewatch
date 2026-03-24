import React from 'react';
import { Link, useParams } from 'react-router-dom';

// ---------------------------------------------------------------------------
// Mock capture detail – replace / augment with an API call in production
// ---------------------------------------------------------------------------
const MOCK_DETAILS = {
  c1: {
    id: 'c1',
    url: 'https://www.acme.com/pricing',
    capturedAt: '2026-03-24T15:33:59',
    category: 'pricing',
    importance: 0.92,
    summary:
      'Enterprise plan price increased from $99/mo to $129/mo. New "Growth" tier added at $79/mo. Annual discount changed from 20% to 15%.',
    diff: `--- a/page.html\t2026-03-23 08:00:00.000000000 +0000
+++ b/page.html\t2026-03-24 15:33:59.000000000 +0000
@@ -14,7 +14,7 @@
     <div class="pricing-hero">
-      <h1>Enterprise Plan — $99/mo</h1>
+      <h1>Enterprise Plan — $129/mo</h1>
-      <p>Annual discount: 20% off</p>
+      <p>Annual discount: 15% off</p>
+      <div class="tier new">Growth — $79/mo</div>
    </div>`,
    screenshots: [
      'https://placehold.co/800x450/1e40af/white?text=Before:+Pricing+v1',
      'https://placehold.co/800x450/dc2626/white?text=After:+Pricing+v2',
    ],
  },
  c2: {
    id: 'c2',
    url: 'https://www.acme.com/features',
    capturedAt: '2026-03-24T14:12:01',
    category: 'product',
    importance: 0.65,
    summary:
      'Added new "AI-powered analytics" feature card. Screenshot comparison shows updated hero graphic. "Beta" badge removed from dark mode toggle.',
    diff: `--- a/page.html\t2026-03-24 09:00:00.000000000 +0000
+++ b/page.html\t2026-03-24 14:12:01.000000000 +0000
@@ -22,4 +22,6 @@
+    <div class="feature-card new">
+      <h3>AI-powered Analytics</h3>
+    </div>
     <div class="badge beta">Dark Mode</div>
-    <div class="badge beta">Dark Mode</div>
+    <div class="badge">Dark Mode</div>`,
    screenshots: [
      'https://placehold.co/800x450/1e40af/white?text=Before:+Features',
      'https://placehold.co/800x450/16a34a/white?text=After:+Features',
    ],
  },
  c3: {
    id: 'c3',
    url: 'https://www.acme.com/contact',
    capturedAt: '2026-03-24T12:05:33',
    category: 'contact',
    importance: 0.31,
    summary:
      'Phone number updated from +1-800-555-0100 to +1-800-555-0199. Support email unchanged. Office address remains the same.',
    diff: `--- a/page.html\t2026-03-24 08:00:00.000000000 +0000
+++ b/page.html\t2026-03-24 12:05:33.000000000 +0000
@@ -5,7 +5,7 @@
-    <p class="phone">+1-800-555-0100</p>
+    <p class="phone">+1-800-555-0199</p>
     <p class="email">support@acme.com</p>`,
    screenshots: [
      'https://placehold.co/800x450/374151/white?text=Before:+Contact',
      'https://placehold.co/800x450/374151/white?text=After:+Contact',
    ],
  },
  c4: {
    id: 'c4',
    url: 'https://www.acme.com/legal/terms',
    capturedAt: '2026-03-23T22:01:14',
    category: 'legal',
    importance: 0.88,
    summary:
      'Section 4.2 arbitration clause amended — opt-out window reduced from 30 days to 14 days. New data retention clause added (Section 7.4).',
    diff: `--- a/page.html\t2026-03-22 20:00:00.000000000 +0000
+++ b/page.html\t2026-03-23 22:01:14.000000000 +0000
@@ -44,3 +44,6 @@
-    <p>You may opt out of arbitration within 30 days of accepting these terms.</p>
+    <p>You may opt out of arbitration within 14 days of accepting these terms.</p>
+  </div>
+  <div class="section" id="7.4">
+    <h2>7.4 Data Retention</h2>`,
    screenshots: [
      'https://placehold.co/800x450/78350f/white?text=Before:+Terms',
      'https://placehold.co/800x450/78350f/white?text=After:+Terms',
    ],
  },
  c5: {
    id: 'c5',
    url: 'https://www.acme.com/',
    capturedAt: '2026-03-23T18:44:02',
    category: 'product',
    importance: 0.44,
    summary:
      'Navigation bar reordered — "Pricing" moved from 3rd to 1st position. CTA button text changed from "Get Started" to "Start Free Trial".',
    diff: `--- a/page.html\t2026-03-23 08:00:00.000000000 +0000
+++ b/page.html\t2026-03-23 18:44:02.000000000 +0000
@@ -2,9 +2,9 @@
   <nav>
-    <a href="/">Home</a>
-    <a href="/features">Features</a>
-    <a href="/pricing">Pricing</a>
+    <a href="/pricing">Pricing</a>
+    <a href="/">Home</a>
+    <a href="/features">Features</a>
    </nav>
-  <button>Get Started</button>
+  <button>Start Free Trial</button>`,
    screenshots: [
      'https://placehold.co/800x450/1e40af/white?text=Before:+Homepage',
      'https://placehold.co/800x450/16a34a/white?text=After:+Homepage',
    ],
  },
  c6: {
    id: 'c6',
    url: 'https://www.acme.com/changelog',
    capturedAt: '2026-03-23T09:30:00',
    category: 'other',
    importance: 0.18,
    summary:
      'Changelog entry added for v2.4.1 patch release — "Fixed intermittent login timeout on Safari". No content structural changes.',
    diff: `--- a/page.html\t2026-03-23 08:00:00.000000000 +0000
+++ b/page.html\t2026-03-23 09:30:00.000000000 +0000
@@ -30,3 +30,5 @@
+  <li>v2.4.1 — Fixed intermittent login timeout on Safari.</li>
   </ul>`,
    screenshots: [
      'https://placehold.co/800x450/374151/white?text=Before:+Changelog',
      'https://placehold.co/800x450/374151/white?text=After:+Changelog',
    ],
  },
  c7: {
    id: 'c7',
    url: 'https://www.acme.com/privacy',
    capturedAt: '2026-03-22T20:15:45',
    category: 'legal',
    importance: 0.95,
    summary:
      'Data sharing section rewritten — third-party广告 partners now explicitly named. New checkbox opt-in required for analytics cookies.',
    diff: `--- a/page.html\t2026-03-22 08:00:00.000000000 +0000
+++ b/page.html\t2026-03-22 20:15:45.000000000 +0000
@@ -18,7 +18,12 @@
-    <p>We do not share your data with third parties.</p>
+    <p>We share data with the following partners: Google Analytics, Meta Pixel, Segment, Amplitude.</p>
+    <div class="cookie-consent">
+      <input type="checkbox" id="analytics-opt-in" />
+      <label for="analytics-opt-in">I consent to analytics cookies</label>
+    </div>`,
    screenshots: [
      'https://placehold.co/800x450/78350f/white?text=Before:+Privacy',
      'https://placehold.co/800x450/dc2626/white?text=After:+Privacy',
    ],
  },
  c8: {
    id: 'c8',
    url: 'https://www.acme.com/pricing',
    capturedAt: '2026-03-22T08:00:10',
    category: 'pricing',
    importance: 0.87,
    summary:
      'Free tier minutes reduced from 1000 to 500 per month. Overage pricing added: $0.004/min. Page layout refactored with new tier comparison table.',
    diff: `--- a/page.html\t2026-03-21 08:00:00.000000000 +0000
+++ b/page.html\t2026-03-22 08:00:10.000000000 +0000
@@ -10,9 +10,11 @@
-    <div class="tier free">Free — 1000 min/mo</div>
+    <div class="tier free">Free — 500 min/mo</div>
+    <p class="overage">Overage: $0.004/min</p>
-    <table class="comparison"><!-- old table --></table>
+    <table class="comparison"><!-- new table --></table>`,
    screenshots: [
      'https://placehold.co/800x450/1e40af/white?text=Before:+Pricing+v1',
      'https://placehold.co/800x450/dc2626/white?text=After:+Pricing+v2',
    ],
  },
};

// ---------------------------------------------------------------------------
// Diff viewer – side-by-side using pre/code blocks
// ---------------------------------------------------------------------------
function DiffViewer({ diff }) {
  if (!diff) {
    return (
      <p style={{ color: '#6b7280', fontStyle: 'italic', fontSize: 13 }}>
        No diff available for this capture.
      </p>
    );
  }

  const lines = diff.split('\n');

  return (
    <div
      style={{
        border: '1px solid #e5e7eb',
        borderRadius: 8,
        overflow: 'hidden',
        fontSize: 12,
        fontFamily: "'Menlo', 'Consolas', monospace",
      }}
    >
      {/* Column headers */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          background: '#f3f4f6',
          borderBottom: '1px solid #e5e7eb',
          fontSize: 11,
          fontWeight: 700,
          color: '#6b7280',
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
        }}
      >
        <div style={{ padding: '6px 12px', borderRight: '1px solid #e5e7eb' }}>Before</div>
        <div style={{ padding: '6px 12px' }}>After</div>
      </div>

      {/* Side-by-side diff lines */}
      <div style={{ overflowX: 'auto' }}>
        <table style={{ borderCollapse: 'collapse', width: '100%' }}>
          <tbody>
            {lines.map((line, i) => {
              const isAdded = line.startsWith('+') && !line.startsWith('+++');
              const isRemoved = line.startsWith('-') && !line.startsWith('---');
              const isContext = !isAdded && !isRemoved && !line.startsWith('@@') && !line.startsWith('\\');
              const isHunk = line.startsWith('@@');

              let bg = 'transparent';
              let prefixColor = '#6b7280';
              if (isAdded) { bg = '#dcfce7'; prefixColor = '#166534'; }
              if (isRemoved) { bg = '#fee2e2'; prefixColor = '#991b1b'; }
              if (isHunk) { bg = '#fef9c3'; prefixColor = '#854d0e'; }

              const displayLine = line.replace(/^[+-]{1,3}/, '');

              return (
                <tr key={i} style={{ background: bg }}>
                  {/* Left column – only shows removed/context lines */}
                  <td
                    style={{
                      padding: '1px 12px',
                      color: isRemoved ? '#991b1b' : '#6b7280',
                      whiteSpace: 'pre',
                      minWidth: '50%',
                      borderRight: '1px solid #e5e7eb',
                    }}
                  >
                    {(isRemoved || isContext || isHunk) ? line : ''}
                  </td>
                  {/* Right column – only shows added/context lines */}
                  <td
                    style={{
                      padding: '1px 12px',
                      color: isAdded ? '#166534' : '#6b7280',
                      whiteSpace: 'pre',
                      minWidth: '50%',
                    }}
                  >
                    {(isAdded || isContext || isHunk) ? line : ''}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Screenshot gallery
// ---------------------------------------------------------------------------
function ScreenshotGallery({ screenshots }) {
  if (!screenshots || screenshots.length === 0) {
    return (
      <p style={{ color: '#6b7280', fontStyle: 'italic', fontSize: 13 }}>
        No screenshots available for this capture.
      </p>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
      {screenshots.map((src, i) => (
        <div key={i}>
          <p style={{ fontSize: 11, fontWeight: 600, color: '#6b7280', textTransform: 'uppercase', marginBottom: 6 }}>
            {i === 0 ? 'Before' : 'After'}
          </p>
          <img
            src={src}
            alt={`Screenshot ${i + 1}`}
            style={{
              width: '100%',
              maxWidth: 600,
              borderRadius: 6,
              border: '1px solid #e5e7eb',
              display: 'block',
            }}
          />
        </div>
      ))}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
const CATEGORY_COLORS = {
  pricing: { bg: '#fee2e2', text: '#991b1b', border: '#fca5a5' },
  product: { bg: '#dbeafe', text: '#1e40af', border: '#93c5fd' },
  contact: { bg: '#dcfce7', text: '#166534', border: '#86efac' },
  legal: { bg: '#ffedd5', text: '#9a3412', border: '#fdba74' },
  other: { bg: '#f3f4f6', text: '#374151', border: '#d1d5db' },
};

function CategoryBadge({ category }) {
  const colors = CATEGORY_COLORS[category] || CATEGORY_COLORS.other;
  return (
    <span
      style={{
        display: 'inline-block',
        padding: '3px 10px',
        borderRadius: 9999,
        fontSize: 12,
        fontWeight: 700,
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

function ImportancePill({ value }) {
  const pct = Math.round(value * 100);
  const color = pct >= 75 ? '#ef4444' : pct >= 40 ? '#f59e0b' : '#22c55e';
  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: 6,
        padding: '3px 10px',
        borderRadius: 9999,
        fontSize: 12,
        fontWeight: 600,
        background: color + '22',
        color: color,
        border: `1px solid ${color}66`,
      }}
    >
      <span
        style={{
          width: 6,
          height: 6,
          borderRadius: '50%',
          background: color,
          display: 'inline-block',
        }}
      />
      {pct}% importance
    </span>
  );
}

function formatTimestamp(iso) {
  return new Date(iso).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
}

// ---------------------------------------------------------------------------
// Evidence view page
// ---------------------------------------------------------------------------
export default function EvidenceView() {
  const { id } = useParams();
  const capture = MOCK_DETAILS[id];

  if (!capture) {
    return (
      <div
        style={{
          minHeight: '100vh',
          background: '#f9fafb',
          fontFamily: 'system-ui, sans-serif',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <div style={{ textAlign: 'center' }}>
          <h2 style={{ color: '#374151' }}>Capture not found</h2>
          <p style={{ color: '#6b7280' }}>
            No capture with ID <code>{id}</code>
          </p>
          <Link
            to="/"
            style={{
              marginTop: 16,
              display: 'inline-block',
              color: '#3b82f6',
              textDecoration: 'underline',
              fontSize: 14,
            }}
          >
            ← Back to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: '100vh', background: '#f9fafb', fontFamily: 'system-ui, sans-serif' }}>
      {/* Header */}
      <header
        style={{
          background: '#111827',
          color: '#fff',
          padding: '14px 24px',
          display: 'flex',
          alignItems: 'center',
          gap: 16,
        }}
      >
        <Link
          to="/"
          style={{
            color: '#9ca3af',
            textDecoration: 'none',
            fontSize: 13,
            display: 'flex',
            alignItems: 'center',
            gap: 4,
          }}
        >
          ← Dashboard
        </Link>
        <div style={{ width: 1, height: 16, background: '#374151' }} />
        <span style={{ fontSize: 13, fontFamily: 'monospace', color: '#d1d5db' }}>
          Evidence: {id}
        </span>
      </header>

      <div style={{ maxWidth: 900, margin: '0 auto', padding: '24px' }}>
        {/* Metadata card */}
        <div
          style={{
            background: '#fff',
            border: '1px solid #e5e7eb',
            borderRadius: 8,
            padding: '20px 24px',
            marginBottom: 16,
          }}
        >
          {/* URL + badges */}
          <div style={{ display: 'flex', alignItems: 'flex-start', gap: 10, flexWrap: 'wrap', marginBottom: 14 }}>
            <CategoryBadge category={capture.category} />
            <ImportancePill value={capture.importance} />
          </div>

          <div style={{ marginBottom: 10 }}>
            <p style={{ fontSize: 11, fontWeight: 700, color: '#6b7280', textTransform: 'uppercase', margin: '0 0 2px' }}>
              Target URL
            </p>
            <code
              style={{
                fontSize: 13,
                color: '#374151',
                background: '#f3f4f6',
                padding: '2px 6px',
                borderRadius: 4,
                wordBreak: 'break-all',
              }}
            >
              {capture.url}
            </code>
          </div>

          <div style={{ marginBottom: 14 }}>
            <p style={{ fontSize: 11, fontWeight: 700, color: '#6b7280', textTransform: 'uppercase', margin: '0 0 2px' }}>
              Captured At
            </p>
            <p style={{ fontSize: 13, color: '#374151', margin: 0 }}>{formatTimestamp(capture.capturedAt)}</p>
          </div>

          <div>
            <p style={{ fontSize: 11, fontWeight: 700, color: '#6b7280', textTransform: 'uppercase', margin: '0 0 4px' }}>
              Summary
            </p>
            <p
              style={{
                fontSize: 14,
                color: '#1f2937',
                margin: 0,
                lineHeight: 1.6,
                background: '#f9fafb',
                padding: '10px 14px',
                borderRadius: 6,
                border: '1px solid #e5e7eb',
              }}
            >
              {capture.summary}
            </p>
          </div>
        </div>

        {/* Diff viewer */}
        <div style={{ marginBottom: 16 }}>
          <h2
            style={{
              fontSize: 14,
              fontWeight: 700,
              color: '#374151',
              textTransform: 'uppercase',
              letterSpacing: '0.05em',
              marginBottom: 10,
            }}
          >
            Diff Viewer
          </h2>
          <DiffViewer diff={capture.diff} />
        </div>

        {/* Screenshots */}
        <div>
          <h2
            style={{
              fontSize: 14,
              fontWeight: 700,
              color: '#374151',
              textTransform: 'uppercase',
              letterSpacing: '0.05em',
              marginBottom: 10,
            }}
          >
            Screenshots
          </h2>
          <ScreenshotGallery screenshots={capture.screenshots} />
        </div>
      </div>
    </div>
  );
}
