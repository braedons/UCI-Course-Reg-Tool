const { classesDb } = require('../db')

class ClassesServices {
	static getOverlap(comparand1, comparand2) {
		let list1 = classesDb.getClassList(comparand1);
		let list2 = classesDb.getClassList(comparand2);

		if (list1 == null) {
			throw "Comparand 1 wasn't found";
		}
		if (list2 == null) {
			throw "Comparand 2 wasn't found";
		}

		return [...list1].filter(elem => list2.has(elem));
	}
}

module.exports = {
	ClassesServices
}