var express = require('express');
var router = express.Router();

comparandMap = {'GE': new Set(['cs 1', 'cs 2']), 'CS': new Set(['cs 1', 'cs 3'])}

router.get('/overlap', (req, res, next) => {
	var comparand1 = req.query.comparand1;
	var comparand2 = req.query.comparand2;

	if (comparand1 == null || comparand2 == null) {
		res.send("missing comparands");
		return;
	}

	try {
		overlapList = findOverlap(comparand1, comparand2);

		res.send({
			comparand1: comparand1,
			comparand2: comparand2,
			overlapList: overlapList
		});
	}
	catch (e) {
		res.send("ERROR: " + e);
	}
});

function getClassList(comparand) {
	return comparandMap[comparand];
}

function findOverlap(comparand1, comparand2) {
	list1 = getClassList(comparand1);
	list2 = getClassList(comparand2);

	if (list1 == null || list2 == null) {
		throw "Comparands weren't found";
	}

	return [...list1].filter(elem => list2.has(elem));
}

module.exports = router;