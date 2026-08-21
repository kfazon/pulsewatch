<?php
// PulseWatch managed-pilot lead capture.
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: https://pulsewatch.top');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

$subscribers_file = getenv('PULSEWATCH_SUBSCRIBERS_FILE') ?: '';
if ($subscribers_file === '' || $subscribers_file[0] !== '/') {
    http_response_code(503);
    echo json_encode(['success' => false, 'message' => 'Signup is temporarily unavailable']);
    exit;
}

$target_dir = realpath(dirname($subscribers_file));
$public_dir = realpath(__DIR__);
if (
    $target_dir === false ||
    $public_dir === false ||
    $target_dir === $public_dir ||
    str_starts_with($target_dir . DIRECTORY_SEPARATOR, $public_dir . DIRECTORY_SEPARATOR)
) {
    http_response_code(503);
    echo json_encode(['success' => false, 'message' => 'Signup is temporarily unavailable']);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);
if (!is_array($input) || !isset($input['email'])) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Email is required']);
    exit;
}

$email = filter_var(trim((string) $input['email']), FILTER_VALIDATE_EMAIL);
if (!$email) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Invalid email address']);
    exit;
}

$handle = @fopen($subscribers_file, 'c+');
if ($handle === false || !flock($handle, LOCK_EX)) {
    if (is_resource($handle)) {
        fclose($handle);
    }
    http_response_code(503);
    echo json_encode(['success' => false, 'message' => 'Signup is temporarily unavailable']);
    exit;
}

$raw = stream_get_contents($handle);
$subscribers = $raw === '' ? [] : json_decode($raw, true);
if (!is_array($subscribers)) {
    $subscribers = [];
}

// Enforce the published 90-day retention window for unconverted pilot leads.
$retention_cutoff = time() - (90 * 24 * 60 * 60);
$subscribers = array_values(array_filter(
    $subscribers,
    static function ($subscriber) use ($retention_cutoff): bool {
        if (!is_array($subscriber) || !isset($subscriber['subscribed_at'])) {
            return false;
        }
        $timestamp = strtotime((string) $subscriber['subscribed_at']);
        return $timestamp !== false && $timestamp >= $retention_cutoff;
    }
));

foreach ($subscribers as $subscriber) {
    if (isset($subscriber['email']) && strcasecmp((string) $subscriber['email'], $email) === 0) {
        flock($handle, LOCK_UN);
        fclose($handle);
        echo json_encode(['success' => true, 'message' => 'You are already registered']);
        exit;
    }
}

$subscribers[] = [
    'email' => $email,
    'subscribed_at' => date('c'),
];

$encoded = json_encode($subscribers, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
if ($encoded === false) {
    flock($handle, LOCK_UN);
    fclose($handle);
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Could not save signup']);
    exit;
}

rewind($handle);
if (!ftruncate($handle, 0) || fwrite($handle, $encoded . PHP_EOL) === false || !fflush($handle)) {
    flock($handle, LOCK_UN);
    fclose($handle);
    http_response_code(503);
    echo json_encode(['success' => false, 'message' => 'Signup is temporarily unavailable']);
    exit;
}

@chmod($subscribers_file, 0600);
flock($handle, LOCK_UN);
fclose($handle);

echo json_encode([
    'success' => true,
    'message' => 'Thanks. We will review fit and send the pilot details.',
]);
