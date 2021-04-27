var mysql = require('mysql');

class ClassesDB {
	constructor() {
		this.comparandMap = { 'GE': new Set(['cs 1', 'cs 2']), 'CS': new Set(['cs 1', 'cs 3']) };

		let con = mysql.createConnection({
			host: "localhost",
			user: "braedons",
			password: "test"
		});

		con.connect(function (err) {
			if (err) throw err;
			console.log("Connected!");
		});
	}

	getClassList(comparand) {
		return this.comparandMap[comparand]; // TODO: ignore case
	}
}

classesDb = new ClassesDB();
module.exports = {
	classesDb
};