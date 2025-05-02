const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// Store requests for verification
const requests = [];

// Mock audio transcription endpoint
app.post('/v1/audio/transcriptions', (req, res) => {
  requests.push({
    type: 'transcription',
    body: req.body
  });

  res.json({
    text: "This is a mock transcription of the audio file."
  });
});

// Mock chat completion endpoint
app.post('/v1/chat/completions', (req, res) => {
  requests.push({
    type: 'chat',
    body: req.body
  });

  res.json({
    id: 'mock-completion-id',
    object: 'chat.completion',
    created: Date.now(),
    model: req.body.model,
    choices: [{
      index: 0,
      message: {
        role: 'assistant',
        content: 'This is a mock response from the assistant.'
      },
      finish_reason: 'stop'
    }]
  });
});

// Endpoint to get stored requests for verification
app.get('/_test/requests', (req, res) => {
  res.json(requests);
});

// Endpoint to clear stored requests
app.post('/_test/clear', (req, res) => {
  requests.length = 0;
  res.json({ ok: true });
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`OpenAI mock server running on port ${port}`);
});
