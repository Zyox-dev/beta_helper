<?php
header('Content-Type: application/json');

// Ensure request is POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method Not Allowed']);
    exit;
}

$input = file_get_contents('php://input');
$data = json_decode($input, true);

if (!$data || !isset($data['contents'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid JSON input']);
    exit;
}

// Secured API key on the backend
$apiKey = getenv('GEMINI_API_KEY') ?: 'AQ.Ab8RN6L_7g-_EUd1-OVPxTm-kduCsklFtuheseAfMBrp4jvCXQ';
$endpoint = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent';

$ch = curl_init($endpoint);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'X-goog-api-key: ' . $apiKey
]);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode([
    'contents' => $data['contents']
]));
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($response === false || $httpCode !== 200) {
    http_response_code($httpCode ?: 500);
    echo json_encode(['error' => 'Gemini API call failed', 'details' => $response]);
    exit;
}

echo $response;
