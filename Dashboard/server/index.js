const express = require('express');
const app = express();
const cors = require('cors');
const pool = require('./db');

app.use(cors());
app.use(express.json());

// Get Raw Stats
app.get('*', async(req, res) => {
	try{
		const BaseballData = await pool.query('SELECT * FROM public."AL"UNION ALL SELECT * FROM public."NL"');
		res.json(BaseballData.rows);
	} catch (err) {
		console.error(err.message);
	}
});

app.listen(5000, () =>{
	console.log('server has started on port: 5000');
});


