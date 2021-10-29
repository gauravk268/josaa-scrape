const express = require("express");
const mongoose = require("mongoose");
const moment = require("moment");
const cors = require("cors");

moment().utcOffset("+05:30").format();

const app = express();
app.use(cors());

const logActivity = (value) => {
  const output = moment().format("ddd:DD-MM-YYYYTHH:mm:ss ") + value;
  console.log(output);
};

const connectDB = () => {
  // const URL = process.env.MONGO_URL;
  const URL = "http://localhost:27017";
  logActivity("[mongoose] connecting to db: " + URL);

  try {
    mongoose.connect(URL, () => {
      logActivity("[mongoose] connected to db");
    });
  } catch (error) {
    logActivity("[mongoose] cannot connect to db: ", error);
  }
};

const closeConnection = () => {
  logActivity("[mongoose] closed connection to db");
};

connectDB();
// closeConnection();

app.get("/", (req, res) => {
  res.status(200).sendFile(__dirname + "/views/homepage.html" );
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  logActivity(`[express] josaa-clg-backend server running on port ${PORT}`);
});
