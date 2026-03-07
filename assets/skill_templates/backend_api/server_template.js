import express from 'express';
import cors from 'cors';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Routes
app.get('/api/status', (req, res) => {
    res.json({ status: 'ok', message: 'Backend API is running' });
});

app.post('/api/process', (req, res) => {
    const data = req.body;

    if (!data) {
        return res.status(400).json({ error: 'No data provided' });
    }

    // Custom logic here
    res.json({ result: 'processed', original: data });
});

app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}`);
});
