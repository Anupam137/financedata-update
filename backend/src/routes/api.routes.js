const express = require('express');
const queryController = require('../controllers/query.controller');

const router = express.Router();

/**
 * @route POST /api/query
 * @desc Process a financial query (including comparisons)
 * @access Public
 */
router.post('/query', queryController.processQuery);

/**
 * @route DELETE /api/conversation/:sessionId
 * @desc Clear conversation history
 * @access Public
 */
router.delete('/conversation/:sessionId', queryController.clearConversation);

/**
 * @route GET /api/news/:topic
 * @desc Get latest news and market sentiment about a topic
 * @access Public
 */
router.get('/news/:topic', queryController.getMarketNews);

module.exports = router; 