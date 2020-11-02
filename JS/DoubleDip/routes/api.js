const express = require('express');
const router = express.Router();
const { ClassesController } = require('../controllers');

router.get('/overlap', ClassesController.overlap);

module.exports = router;