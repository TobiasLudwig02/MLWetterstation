const express = require('express');
const bodyParser = require('body-parser');
const { Connection, Request } = require('tedious');

const app = express();
app.use(bodyParser.json());

// Azure SQL Database connection configuration
const config = {
  authentication: {
    options: {
      userName: process.env.DB_USER,
      password: process.env.DB_PASSWORD
    },
    type: 'default'
  },
  server: process.env.DB_SERVER,
  options: {
    database: process.env.DB_NAME,
    encrypt: true
  }
};

app.post('/sensordata', (req, res) => {
  const { temperature, humidity } = req.body;

  const connection = new Connection(config);

  connection.on('connect', err => {
    if (err) {
      console.error('Connection failed', err);
      res.status(500).send('Database connection failed');
    } else {
      const query = `INSERT INTO SensorData (Temperature, Humidity) VALUES (${temperature}, ${humidity})`;
      const request = new Request(query, (err, rowCount) => {
        if (err) {
          console.error('Insert failed', err);
          res.status(500).send('Insert failed');
        } else {
          res.status(200).send('Data inserted successfully');
        }
        connection.close();
      });

      connection.execSql(request);
    }
  });

  connection.connect();
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
