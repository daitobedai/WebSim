<?php 
// 建立客户端的socet连接 
$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP); 
  //连接服务器端socket 

$connection = socket_connect($socket, '127.0.0.1', 9999);  
//要发送到服务端的信息。
$send_data = "This data will Send to server!";
echo "doudou\n";
//客户端去连接服务端并接受服务端返回的数据，如果返回的数据保护not connect就提示不能连接。
        // 将客户的信息写到通道中，传给服务器端 
        while(socket_write($socket, "$send_data\n")){ 
            $buffer = @socket_read($socket, 1024);
            echo "Buffer Data: " . $buffer . "\n";
        } 
  
?>