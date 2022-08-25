const Pool = require('pg').Pool;

const pool = new Pool({
	user: 'postgres',
	password: 'CSCboi*!69',
	host: 'localhost',
	port: 5432,
	database: 'Raw_Stats'
})

module.exports = pool;
