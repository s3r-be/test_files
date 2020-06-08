<?php

$loop = React\EventLoop\Factory::create();
$socket = new React\Socket\Server('0.0.0.0:12345', $loop);

$socket->on('connection', function (React\Socket\ConnectionInterface $connection) {
    $connection->write("Hello " . $connection->getRemoteAddress() . "!\n");
    $connection->write("Welcome to this amazing server!\n");
    $connection->write("Here's a tip: don't say anything.\n");

    $connection->on('data', function ($data) use ($connection) {
        $data = file_get_contents('http://localhost/ids/datastorage.txt');
        $connection->write($data);
        $connection->close();
    });
});

$loop->run();