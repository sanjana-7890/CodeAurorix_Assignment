const WebSocket = require('ws');
const os = require('os');

const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', (ws) => {
  console.log('Client connected');

  // Function to send messages every 5 seconds
  const sendMessages = () => {
    setInterval(() => {
      const ipAddress = getIpAddress();
      const message = `Hello from ${ipAddress}!`;
      ws.send(message);
    }, 5000); // Send a message every 5 seconds (5000 milliseconds)
  };

  // Call the function to start sending messages
  sendMessages();

  // Handle incoming messages from clients
  ws.on('message', (message) => {
    console.log(`Received message: ${message}`);
  });

  // Handle client disconnection
  ws.on('close', () => {
    console.log('Client disconnected');
  });
});

console.log('WebSocket server is listening on port 8080');

// Function to get IP address of the current container
function getIpAddress() {
  const interfaces = os.networkInterfaces();
  for (const ifaceName of Object.keys(interfaces)) {
    for (const iface of interfaces[ifaceName]) {
      if (iface.family === 'IPv4' && !iface.internal) {
        return iface.address;
      }
    }
  }
  return 'unknown';
}

