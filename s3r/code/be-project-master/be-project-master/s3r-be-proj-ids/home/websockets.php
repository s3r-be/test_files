
<?php

$address = '0.0.0.0';
$port = 12345;
$MAX_RECONNECTION_ATTEMPTS = 15;
$server = '';
$client = '';

// Create WebSocket.
function createWebsocket() {
    global $server, $client, $address, $port;
    $server = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
    if ($server) echo 'Socket created' . PHP_EOL;
    socket_set_option($server, SOL_SOCKET, SO_REUSEADDR, 1);
    socket_bind($server, $address, $port);
    $is_listening = socket_listen($server);
    if ($is_listening) echo 'Listening on port ' . $port . PHP_EOL;
    $client = socket_accept($server);
    echo 'Accepted client: ' . $client . PHP_EOL;

    // Send WebSocket handshake headers.
    $request = socket_read($client, 5000);
    echo 'Received request'  . PHP_EOL . $request . PHP_EOL;
    
    preg_match('#Sec-WebSocket-Key: (.*)\r\n#', $request, $matches);
    $key = base64_encode(pack('H*', sha1($matches[1] . '258EAFA5-E914-47DA-95CA-C5AB0DC85B11')));
    $headers = "HTTP/1.1 101 Switching Protocols\r\n";
    $headers .= "Upgrade: websocket\r\n";
    $headers .= "Connection: Upgrade\r\n";
    $headers .= "Sec-WebSocket-Version: 13\r\n";
    $headers .= "Sec-WebSocket-Accept: $key\r\n\r\n";
    socket_write($client, $headers, strlen($headers));
}

createWebsocket();

$reconnection_attempts = 0;

// Send messages into WebSocket in a loop.
while ($reconnection_attempts < $MAX_RECONNECTION_ATTEMPTS) {
    sleep(1);
    $data = file_get_contents('http://localhost/ids/datastorage.txt');
    $content = $data;
    $response = chr(129) . chr(strlen($content)) . $content;
    $writeResult = socket_write($client, $response);
    if ( $writeResult === FALSE ) {
        // got a broken pipe
        echo PHP_EOL . 'closing socket' . PHP_EOL;
        socket_close($server);
        // recreate socket - reconnection
        echo 're-establishing connection with socket' . PHP_EOL;
        createWebsocket();
        // increment reconnection attempt
        $reconnection_attempts++;
        echo 'done with attempt: ' . $reconnection_attempts . PHP_EOL;
    }
}

echo 'Exceeded max reconnection attempts';
socket_close($server);
