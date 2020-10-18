var express = require('express');
var router = express.Router();

router.get('/', (req, res, next) => {
	var cat1 = res.get('cat1');
	var cat2 = res.get('cat2');
	res.send(cat1 + " " + cat2);
});

module.exports = router;