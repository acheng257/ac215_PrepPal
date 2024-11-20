'use client';

import React, { useState, useEffect, useRef } from 'react';
import styles from './styles.module.css';
import Header from '@/components/layout/Header';
import { useRouter } from 'next/navigation';
import DataService from '@/services/DataService';

const PrepPal = () => {
  const [filters, setFilters] = useState({
    cookingTime: 30,
    servings: 4,
    cuisine: 'all',
    ingredients: []
  });
  const [recommendations, setRecommendations] = useState([]);
  const [chatMessage, setChatMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [chatId, setChatId] = useState(null);
  const [isTyping, setIsTyping] = useState(false);
  const router = useRouter();
  const chatHistoryRef = useRef(null);
  const [userId, setUserId] = useState(DataService.GetUser());

  // Auto-scroll to the bottom of chat history
  const scrollToBottom = () => {
    if (chatHistoryRef.current) {
      chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
    }
  };

  useEffect(() => {
    if (chatId) {
      fetchChat(chatId);
    }
  }, [chatId]);

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory]); // Scroll to bottom when chatHistory updates

  async function fetchUserPantry(userId) {
    try {
      const response = await DataService.GetPantry(userId);
      console.log("Pantry data:", response.data);
      return response.data;
    } catch (error) {
      console.error("Failed to fetch pantry data:", error.message || error.response?.data);
    }
  }

  const fetchChat = async (id) => {
    try {
      setIsTyping(true);
      const response = await DataService.GetChat('llm', id);
      setChatHistory(
        response.data.messages.map((msg) => ({
          sender: msg.role === 'user' ? 'User' : 'Bot',
          text: msg.content,
        }))
      );
      setIsTyping(false);
    } catch (error) {
      console.error('Error fetching chat:', error);
      setIsTyping(false);
    }
  };

  const handleSubmit = async () => {
    try {
      console.log(filters);
      const response = await DataService.GetRecipeRecommendation(filters);

      if (response.data) {
        setRecommendations(response.data.recommendations);
      } else {
        alert('Failed to fetch recommendations');
      }
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      alert('An error occurred. Please try again.');
    }
  };

  const handleSendChat = async () => {
    if (!chatMessage.trim()) return;

    const xSessionId = localStorage.getItem('userSessionId');
    if (!xSessionId) {
      alert('User session not found. Please log in.');
      return;
    }

    setChatHistory((prev) => [
      ...prev,
      { sender: 'User', text: chatMessage },
    ]);

    try {
      let response;
      setIsTyping(true);
      const pantry_response = await fetchUserPantry(userId);

      if (!chatId) {
        // Start a new chat
        console.log("starting chat");
        response = await DataService.StartChatWithLLM('llm', { content: chatMessage, recommendations: recommendations, pantry: pantry_response["pantry"] });
        setChatId(response.data.chat_id);
      } else {
        // Continue the existing chat
        console.log("continuing chat");
        response = await DataService.ContinueChatWithLLM('llm', chatId, { content: chatMessage, recommendations: recommendations, pantry: pantry_response["pantry"] });
        console.log("response:", response)
      }

      // Append bot's response to chat history
      const assistantMessage = response.data.messages.filter((msg) => msg.role === 'assistant').pop();

      if (assistantMessage) {
        setChatHistory((prev) => [
          ...prev,
          { sender: 'Bot', text: assistantMessage.content },
        ]);
      }
      setIsTyping(false);
    } catch (error) {
      console.error('Error sending chat message:', error);
      setIsTyping(false);
      alert('An error occurred. Please try again.');
    }

    setChatMessage(''); // Clear input
  };


  const handleRecipeClick = (recipe) => {
    const queryParams = new URLSearchParams({
      name: recipe.title,
      cookingTime: recipe.time,
      calories: recipe.calories,
      ingredients: JSON.stringify(recipe.ingredients),
      instructions: JSON.stringify(recipe.instructions),
    });

    router.push(`/recipe?${queryParams.toString()}`);
  };

  return (
    <div className={styles.appContainer}>
      <Header />

      <main className={styles.mainContent}>
        <div className={styles.gridContainer}>
          <div className={styles.filtersSection}>
            <h2>Filters</h2>
            <div className={styles.filterGroup}>
              <label>Cooking Time</label>
              <input
                type="range"
                min="0"
                max="120"
                value={filters.cookingTime}
                onChange={(e) => setFilters({ ...filters, cookingTime: Number(e.target.value) })}
              />
              <span>{filters.cookingTime} minutes</span>
            </div>
            <div className={styles.filterGroup}>
              <label>Servings</label>
              <input
                type="range"
                min="1"
                max="12"
                value={filters.servings}
                onChange={(e) => setFilters({ ...filters, servings: Number(e.target.value) })}
              />
              <span>{filters.servings} servings</span>
            </div>
            <div className={styles.filterGroup}>
              <label>Cuisine</label>
              <select
                value={filters.cuisine}
                onChange={(e) => setFilters({ ...filters, cuisine: e.target.value })}
              >
                <option value="all">All Cuisines</option>
                <option value="italian">Italian</option>
                <option value="asian">Asian</option>
                <option value="mexican">Mexican</option>
              </select>
            </div>
            <div className={styles.filterGroup}>
              <label>Ingredients</label>
              <input
                type="text"
                placeholder="Enter ingredients separated by commas"
                value={filters.ingredients}
                onChange={(e) => setFilters({
                  ...filters,
                  ingredients: e.target.value.split(',').map((ingredient) => ingredient.trim()),
                })}
              />
              <span>Ingredients: {filters.ingredients.join(', ')}</span>
            </div>
            <button onClick={handleSubmit}>Submit</button>
          </div>

          <div className={styles.recipeGrid}>
            {recommendations.length > 0 ? (
              recommendations.map((recipe, index) => (
                <div
                  key={index}
                  className={styles.recipeCard}
                  onClick={() => handleRecipeClick(recipe)}
                  style={{ cursor: 'pointer' }}
                >
                  <div className={styles.recipeDetails}>
                    <h3>{recipe.title}</h3>
                    <p>Cooking time: {recipe.time}</p>
                    <h4>Missing Ingredients:</h4>
                    <ul>
                      {recipe.missing_ingredients.map((ingredient, idx) => (
                        <li key={idx}>• {ingredient}</li>
                      ))}
                    </ul>
                    <p>Calories: {recipe.calories}</p>
                  </div>
                </div>
              ))
            ) : (
              <p className={styles.whiteText}>No recommendations found. Try adjusting the filters and clicking Submit.</p>
            )}
          </div>
        </div>

        <div className={styles.chatbotSection}>
          <div ref={chatHistoryRef} className={styles.chatHistory}>
            {chatHistory.map((message, index) => (
              <div key={index} className={styles.chatMessage}>
                <strong>{message.sender}:</strong> {message.text}
              </div>
            ))}
            {isTyping && <div className={styles.typingIndicator}>Typing...</div>}
          </div>
          <div className={styles.chatInput}>
            <input
              type="text"
              placeholder="Ask about recipes or cooking tips..."
              value={chatMessage}
              onChange={(e) => setChatMessage(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSendChat()}
            />
            <button onClick={handleSendChat}>Send</button>
          </div>
        </div>
      </main>
    </div>
  );
};

export default PrepPal;
