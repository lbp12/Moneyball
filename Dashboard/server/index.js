const express = require('express');
const app = express();
const cors = require('cors');
const pool = require('./db');

app.use(cors());
app.use(express.json());

// Get Raw Stats
app.get('/', async(req, res) => {
	try{
		const BaseballData = await pool.query(`
			SELECT "Name", "Season","H","1B","2B","3B","HR","R","RBI","MVP", 
				"wSB","wRAA","wRC","wRC+","XBH+","WAR","lgID" FROM public."ALLSTATS"
		 			UNION ALL 
		  			SELECT "Name", "Season", "H","1B","2B","3B","HR","R","RBI","MVP", 
						"wSB","wRAA","wRC","wRC+","XBH+","WAR","lgID" FROM public."ALLMVPS";
		`);
		res.json(BaseballData.rows);
	} catch (err) {
		console.error(err.message);
	}
});

app.listen(5000, () =>{
	console.log('server has started on port: 5000');
});


