const { classesDb } = require('../db')

class ClassesServices {
	getOverlap(comparand1, comparand2) {
		list1 = classesDb.getClassList(comparand1);
		list2 = classesDb.getClassList(comparand2);

		if (list1 == null || list2 == null) {
			throw "Comparands weren't found";
		}

		return [...list1].filter(elem => list2.has(elem));
	}
}

module.exports = {
	ClassesServices
}