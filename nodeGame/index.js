const express = require('express');

const app = express();

const port = 7777;

app.get('/', (req, res) =>
    {
        res.send("Test Page");
    });

app.listen(port, () =>
    {
        console.log('Express server listening on port ${port}!');
    });
