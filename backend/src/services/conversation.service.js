/**
 * Conversation Manager Service
 * Handles storing and retrieving conversation history
 */

// In-memory store for conversations (in production, use a database)
const conversations = new Map();

// Maximum conversation history length
const MAX_CONVERSATION_LENGTH = 20;

/**
 * Create a new conversation or get an existing one
 * @param {string} sessionId - Unique identifier for the conversation
 * @returns {object} - Conversation object
 */
function getOrCreateConversation(sessionId) {
  if (!conversations.has(sessionId)) {
    conversations.set(sessionId, {
      messages: [],
      createdAt: new Date(),
      lastUpdated: new Date()
    });
  }
  
  return conversations.get(sessionId);
}

/**
 * Add a message to the conversation history
 * @param {string} sessionId - Unique identifier for the conversation
 * @param {string} role - Message role (user, assistant, system)
 * @param {string} content - Message content
 * @returns {array} - Updated conversation messages
 */
function addMessage(sessionId, role, content) {
  const conversation = getOrCreateConversation(sessionId);
  
  // Add the new message
  conversation.messages.push({
    role,
    content
  });
  
  // Trim conversation if it exceeds maximum length
  if (conversation.messages.length > MAX_CONVERSATION_LENGTH) {
    // Keep the first system message if it exists
    const systemMessage = conversation.messages.find(msg => msg.role === 'system');
    
    // Remove oldest messages but keep the most recent ones
    conversation.messages = conversation.messages.slice(-MAX_CONVERSATION_LENGTH);
    
    // Add back the system message at the beginning if it was removed
    if (systemMessage && !conversation.messages.some(msg => msg.role === 'system')) {
      conversation.messages.unshift(systemMessage);
    }
  }
  
  // Update last updated timestamp
  conversation.lastUpdated = new Date();
  
  return conversation.messages;
}

/**
 * Get the conversation history
 * @param {string} sessionId - Unique identifier for the conversation
 * @returns {array} - Conversation messages
 */
function getConversationHistory(sessionId) {
  const conversation = getOrCreateConversation(sessionId);
  return conversation.messages;
}

/**
 * Clear the conversation history
 * @param {string} sessionId - Unique identifier for the conversation
 * @returns {boolean} - Success status
 */
function clearConversation(sessionId) {
  if (conversations.has(sessionId)) {
    const conversation = conversations.get(sessionId);
    conversation.messages = [];
    conversation.lastUpdated = new Date();
    return true;
  }
  return false;
}

/**
 * Clean up old conversations (should be called periodically)
 * @param {number} maxAgeMinutes - Maximum age in minutes
 * @returns {number} - Number of conversations removed
 */
function cleanupOldConversations(maxAgeMinutes = 60) {
  const now = new Date();
  let count = 0;
  
  for (const [sessionId, conversation] of conversations.entries()) {
    const ageMinutes = (now - conversation.lastUpdated) / (1000 * 60);
    
    if (ageMinutes > maxAgeMinutes) {
      conversations.delete(sessionId);
      count++;
    }
  }
  
  return count;
}

module.exports = {
  getOrCreateConversation,
  addMessage,
  getConversationHistory,
  clearConversation,
  cleanupOldConversations
}; 