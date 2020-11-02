comparandMap = { 'GE': new Set(['cs 1', 'cs 2']), 'CS': new Set(['cs 1', 'cs 3']) }

const classesDb = (comparand) => {
	return comparandMap[comparand];
}

module.exports = {
	classesDb
}