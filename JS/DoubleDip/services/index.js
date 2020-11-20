const { ClassesDB } = require('../db')

class ClassesServices {
	static getOverlap(comparand1, comparand2) {
		let list1 = ClassesDB.getClassList(comparand1);
		let list2 = ClassesDB.getClassList(comparand2);

		if (list1 == null || list2 == null) {
			throw "Comparands weren't found";
		}

		return [...list1].filter(elem => list2.has(elem));
	}
}

module.exports = {
	ClassesServices
}