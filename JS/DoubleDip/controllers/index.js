const { ClassesServices } = require('../services');
const { getOverlap } = ClassesServices

class ClassesController {
	overlap(req, res, next) {
		var comparand1 = req.query.comparand1;
		var comparand2 = req.query.comparand2;

		if (comparand1 == null || comparand2 == null) {
			res.send("missing comparands");
			return;
		}

		try {
			overlapList = getOverlap(comparand1, comparand2);

			res.send({
				comparand1: comparand1,
				comparand2: comparand2,
				overlapList: overlapList
			});
		}
		catch (e) {
			res.send("ERROR: " + e);
		}
	}
}

module.exports = {
	ClassesController
}