class ClassesDB {
	static comparandMap = { 'GE': new Set(['cs 1', 'cs 2']), 'CS': new Set(['cs 1', 'cs 3']) }

	static getClassList(comparand) {
		return this.comparandMap[comparand];
	}
}

module.exports = {
	ClassesDB
}