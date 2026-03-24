<?php
/**
 * PulseWatch - Email Subscription Handler
 * 
 * Receives email, logs to subscribers.json, sends Discord notification
 */

header('Content-Type: application/json');

$discord_webhook_url = 'https://discord.com/api/webhooks/1486056242379096134/mIQgGPR_hgyzqj7sCkUkNitFCylafUx1ZIEV57R_dT9JrMDgixDeWiH9c39gD5XlmLPP';
$subscribers_file = __DIR__ . '/subscribers.json';

// Only accept POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Method not allowed']);
    exit;
}

// Parse request body
$input = json_decode(file_get_contents('php://input'), true);

// Handle count request (for landing page dynamic counter)
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($input['action']) && $input['action'] === 'count') {
  $subscribers = [];
  if (file_exists($subscribers_file)) {
    $content = file_get_contents($subscribers_file);
    $subscribers = json_decode($content, true) ?? [];
  }
  echo json_encode(['count' => count($subscribers)]);
  exit;
}

if (!$input || !isset($input['email'])) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Email is required']);
    exit;
}

$email = trim($input['email']);

// Validate email
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Invalid email address']);
    exit;
}

// Load existing subscribers
$subscribers = [];
if (file_exists($subscribers_file)) {
    $content = file_get_contents($subscribers_file);
    $subscribers = json_decode($content, true) ?? [];
}

// Check for duplicate
$emails = array_column($subscribers, 'email');
if (in_array($email, $emails)) {
    echo json_encode(['success' => true, 'message' => 'Already subscribed']);
    exit;
}

// Add new subscriber
$subscriber = [
    'email' => $email,
    'subscribed_at' => date('c'),
    'ip' => $_SERVER['REMOTE_ADDR'] ?? 'unknown',
];
$subscribers[] = $subscriber;

// Save to file
if (file_put_contents($subscribers_file, json_encode($subscribers, JSON_PRETTY_PRINT)) === false) {
    http_response_code(500);
    echo json_encode(['success' => false, 'error' => 'Failed to save subscription']);
    exit;
}

// Send Discord notification
$discord_payload = [
    'content' => '🎯 **New PulseWatch Signup**',
    'embeds' => [
        [
            'title' => 'New Early Adopter',
            'color' => 3447003, // Blue
            'fields' => [
                [
                    'name' => 'Email',
                    'value' => $email,
                    'inline' => true,
                ],
                [
                    'name' => 'Total Subscribers',
                    'value' => (string) count($subscribers),
                    'inline' => true,
                ],
            ],
            'footer' => [
                'text' => 'PulseWatch Landing Page',
            ],
            'timestamp' => date('c'),
        ]
    ]
];

$ch = curl_init($discord_webhook_url);
curl_setopt_array($ch, [
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => json_encode($discord_payload),
    CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT => 10,
]);
$discord_response = curl_exec($ch);
$discord_http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

// Log Discord notification success (optional, don't fail if Discord is down)
if ($discord_http_code !== 204 && $discord_http_code !== 200) {
    error_log("Discord webhook failed with code: $discord_http_code");
}

echo json_encode(['success' => true]);
