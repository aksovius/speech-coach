const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

const VALID_TOKEN = '1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567890';

// Middleware to check token
const checkToken = (req, res, next) => {
  const path = req.path;
  const tokenMatch = path.match(/\/bot([^\/]+)/);
  const token = tokenMatch ? tokenMatch[1] : null;

  if (!token || token !== VALID_TOKEN) {
    return res.status(401).json({
      ok: false,
      error_code: 401,
      description: "Unauthorized"
    });
  }
  next();
};

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// Store messages for verification
const messages = [];

// Mock getFile endpoint
app.get('/bot:token/getFile', checkToken, (req, res) => {
  const fileId = req.query.file_id;
  res.json({
    ok: true,
    result: {
      file_id: fileId,
      file_unique_id: 'unique_' + fileId,
      file_size: 12345,
      file_path: 'voice/test_audio.ogg'
    }
  });
});

// Mock getFile content endpoint
app.get('/file/bot:token/:filePath', checkToken, (req, res) => {
  // Send a mock audio file
  res.sendFile(__dirname + '/test_audio.ogg');
});

// Mock sendMessage endpoint
app.post('/bot:token/sendMessage', checkToken, (req, res) => {
  const message = req.body;
  messages.push(message);
  res.json({
    ok: true,
    result: {
      message_id: messages.length,
      ...message
    }
  });
});

// Mock setWebhook endpoint
app.post('/bot:token/setWebhook', checkToken, (req, res) => {
  res.json({
    ok: true,
    result: true,
    description: "Webhook was set"
  });
});

// Endpoint to get stored messages for verification
app.get('/_test/messages', (req, res) => {
  res.json(messages);
});

// Endpoint to clear stored messages
app.post('/_test/clear', (req, res) => {
  messages.length = 0;
  res.json({ ok: true });
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Telegram mock server running on port ${port}`);
});
