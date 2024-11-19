// 'use client';

// import React, { useEffect, useState } from 'react';
// import styles from './styles.module.css';
// import Header from '@/components/layout/Header';
// import { useRouter } from 'next/navigation';
// import DataService from '@/services/DataService';

// const PrepPal = () => {
//   const [filters, setFilters] = useState({
//     cookingTime: 30,
//     servings: 4,
//     cuisine: 'all',
//     ingredients: []
//   });
//   const [recommendations, setRecommendations] = useState([]);
//   const router = useRouter();
//   const [chatMessage, setChatMessage] = useState('');
//   const [chatHistory, setChatHistory] = useState([]);
//   const [user, setUser] = useState(DataService.GetUser());

//   console.log("user is: ", user)

//   const handleSendChat = async () => {
//     if (!chatMessage) return; // Don't send if there's no message

//     const apiUrl = 'http://localhost:9000/chat_gemini';

//     setChatHistory((prev) => [
//       ...prev,
//       { sender: 'User', text: chatMessage }
//     ]);

//     try {
//       const response = await fetch(apiUrl, {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ message: chatMessage }),
//       });

//       if (response.ok) {
//         const data = await response.json();
//         setChatHistory((prev) => [
//           ...prev,
//           { sender: 'Bot', text: data.response }
//         ]);
//       } else {
//         const errorData = await response.json();
//         alert(errorData.detail || 'Failed to fetch response');
//       }
//     } catch (error) {
//       console.error('Error:', error);
//       alert('An error occurred. Please try again.');
//     }

//     // Clear the chat message input after sending
//     setChatMessage('');
//   };



//   const handleSubmit = async () => {
//     const apiUrl = 'http://localhost:9000/get_recs';

//     try {
//       const response = await fetch(apiUrl, {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ filters, more_recommendations: false }),
//       });

//       if (response.ok) {
//         const data = await response.json();
//         alert("Response ok");
//         setRecommendations(data.recommendations);
//       } else {
//         const errorData = await response.json();
//         alert(errorData.detail || 'Failed to fetch recommendations');
//       }
//     } catch (error) {
//       console.error('Error:', error);
//       alert('An error occurred. Please try again.');
//     }
//   };

//   const handleRecipeClick = (recipe) => {

//     // Manually construct the URL with query parameters
//     const queryParams = new URLSearchParams({
//       name: recipe.name,
//       cookingTime: recipe.cookingTime,
//       calories: recipe.calories,
//       ingredients: JSON.stringify(recipe.ingredients), // Stringify array for URL compatibility
//     });

//     // Use router.push with the constructed URL
//     router.push(`/recipe?${queryParams.toString()}`);
//   };

//   return (
//     <div className={styles.appContainer}>
//       <Header />

//       <main className={styles.mainContent}>
//         <div className={styles.gridContainer}>
//           <div className={styles.filtersSection}>
//             <h2>Filters</h2>
//             <div className={styles.filterGroup}>
//               <label>Cooking Time</label>
//               <input
//                 type="range"
//                 min="0"
//                 max="120"
//                 value={filters.cookingTime}
//                 onChange={(e) => setFilters({ ...filters, cookingTime: Number(e.target.value) })}
//               />
//               <span>{filters.cookingTime} minutes</span>
//             </div>
//             <div className={styles.filterGroup}>
//               <label>Servings</label>
//               <input
//                 type="range"
//                 min="1"
//                 max="12"
//                 value={filters.servings}
//                 onChange={(e) => setFilters({ ...filters, servings: Number(e.target.value) })}
//               />
//               <span>{filters.servings} servings</span>
//             </div>
//             <div className={styles.filterGroup}>
//               <label>Cuisine</label>
//               <select
//                 value={filters.cuisine}
//                 onChange={(e) => setFilters({ ...filters, cuisine: e.target.value })}
//               >
//                 <option value="all">All Cuisines</option>
//                 <option value="italian">Italian</option>
//                 <option value="asian">Asian</option>
//                 <option value="mexican">Mexican</option>
//               </select>
//             </div>
//             <div className={styles.filterGroup}>
//               <label>Ingredients</label>
//               <input
//                 type="text"
//                 placeholder="Enter ingredients separated by commas"
//                 value={filters.ingredients}
//                 onChange={(e) => setFilters({
//                   ...filters,
//                   ingredients: e.target.value.split(',').map(ingredient => ingredient.trim())
//                 })}
//               />
//               <span>Ingredients: {filters.ingredients.join(', ')}</span>
//             </div>
//             <button onClick={handleSubmit}>Submit</button>
//           </div>

//           <div className={styles.recipeGrid}>
//             {recommendations.length > 0 ? (
//               recommendations.map((recipe, index) => (
//                 <div
//                   key={index}
//                   className={styles.recipeCard}
//                   onClick={() => handleRecipeClick(recipe)}
//                   style={{ cursor: 'pointer' }}
//                 >
//                   <div className={styles.recipeDetails}>
//                     <h3>{recipe.name}</h3>
//                     <p>Cooking time: {recipe.cookingTime}</p>
//                     <h4>Ingredients:</h4>
//                     <ul>
//                       {recipe.ingredients.map((ingredient, idx) => (
//                         <li key={idx}>• {ingredient}</li>
//                       ))}
//                     </ul>
//                     <p>Calories: {recipe.calories}</p>
//                   </div>
//                 </div>
//               ))
//             ) : (
//               <p className={styles.whiteText}>No recommendations found. Try adjusting the filters and clicking Submit.</p>
//             )}
//           </div>
//         </div>

//         <div className={styles.chatbotSection}>
//           <div className={styles.chatHistory}>
//             {chatHistory.map((message, index) => (
//               <div key={index} className={styles.chatMessage}>
//                 <strong>{message.sender}:</strong> {message.text}
//               </div>
//             ))}
//           </div>
//           <div className={styles.chatInput}>
//             <input
//               type="text"
//               placeholder="Ask about recipes or cooking tips..."
//               value={chatMessage}
//               onChange={(e) => setChatMessage(e.target.value)}
//             />
//             <button onClick={handleSendChat}>Send</button>
//           </div>
//         </div>
//       </main>
//     </div>
//   );
// };

// export default PrepPal;
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
  const chatHistoryRef = useRef(null); // Ref for chat history container

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
    const apiUrl = `${DataService.BASE_API_URL}/get_recs`;

    try {
      const response = await DataService.api.post(apiUrl, {
        filters,
        more_recommendations: false,
      });

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

      if (!chatId) {
        // Start a new chat
        console.log("starting chat");
        response = await DataService.StartChatWithLLM('llm', { content: chatMessage });
        setChatId(response.data.chat_id);
      } else {
        // Continue the existing chat
        console.log("continuing chat");
        response = await DataService.ContinueChatWithLLM('llm', chatId, { content: chatMessage });
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
      name: recipe.name,
      cookingTime: recipe.cookingTime,
      calories: recipe.calories,
      ingredients: JSON.stringify(recipe.ingredients),
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
                    <h3>{recipe.name}</h3>
                    <p>Cooking time: {recipe.cookingTime}</p>
                    <h4>Ingredients:</h4>
                    <ul>
                      {recipe.ingredients.map((ingredient, idx) => (
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




// 'use client';

// import React, { useState } from 'react';
// import styles from './styles.module.css';
// import Header from '@/components/layout/Header';
// import { useRouter } from 'next/navigation';
// import DataService from '@/services/DataService';

// const PrepPal = () => {
//   const [filters, setFilters] = useState({
//     cookingTime: 30,
//     servings: 4,
//     cuisine: 'all',
//     ingredients: []
//   });
//   const [recommendations, setRecommendations] = useState([]);
//   const [chatMessage, setChatMessage] = useState('');
//   const [chatHistory, setChatHistory] = useState([]);
//   const router = useRouter();

//   const handleSubmit = async () => {
//     const apiUrl = `${DataService.BASE_API_URL}/get_recs`;

//     try {
//       const response = await DataService.api.post(apiUrl, {
//         filters,
//         more_recommendations: false,
//       });

//       if (response.data) {
//         setRecommendations(response.data.recommendations);
//       } else {
//         alert('Failed to fetch recommendations');
//       }
//     } catch (error) {
//       console.error('Error fetching recommendations:', error);
//       alert('An error occurred. Please try again.');
//     }
//   };

//   const handleSendChat = async () => {
//     if (!chatMessage.trim()) return;

//     const model = 'llm'; // Replace with the appropriate model if necessary

//     // Add the user's message to chat history
//     setChatHistory((prev) => [
//       ...prev,
//       { sender: 'User', text: chatMessage }
//     ]);

//     try {
//       let response;
//       if (!chatHistory.length) {
//         // Start a new chat
//         response = await DataService.StartChatWithLLM(model, { content: chatMessage });
//       } else {
//         // Continue the existing chat
//         const lastChatId = chatHistory[chatHistory.length - 1].chat_id;
//         response = await DataService.ContinueChatWithLLM(model, lastChatId, { content: chatMessage });
//       }

//       if (response.data) {
//         // Add the bot's response to chat history
//         setChatHistory((prev) => [
//           ...prev,
//           { sender: 'Bot', text: response.data.response }
//         ]);
//       } else {
//         alert('Failed to get a response from the bot');
//       }
//     } catch (error) {
//       console.error('Error sending chat message:', error);
//       alert('An error occurred. Please try again.');
//     }

//     setChatMessage(''); // Clear the chat input
//   };

//   const handleRecipeClick = (recipe) => {
//     const queryParams = new URLSearchParams({
//       name: recipe.name,
//       cookingTime: recipe.cookingTime,
//       calories: recipe.calories,
//       ingredients: JSON.stringify(recipe.ingredients),
//     });

//     router.push(`/recipe?${queryParams.toString()}`);
//   };

//   return (
//     <div className={styles.appContainer}>
//       <Header />

//       <main className={styles.mainContent}>
//         <div className={styles.gridContainer}>
//           <div className={styles.filtersSection}>
//             <h2>Filters</h2>
//             <div className={styles.filterGroup}>
//               <label>Cooking Time</label>
//               <input
//                 type="range"
//                 min="0"
//                 max="120"
//                 value={filters.cookingTime}
//                 onChange={(e) => setFilters({ ...filters, cookingTime: Number(e.target.value) })}
//               />
//               <span>{filters.cookingTime} minutes</span>
//             </div>
//             <div className={styles.filterGroup}>
//               <label>Servings</label>
//               <input
//                 type="range"
//                 min="1"
//                 max="12"
//                 value={filters.servings}
//                 onChange={(e) => setFilters({ ...filters, servings: Number(e.target.value) })}
//               />
//               <span>{filters.servings} servings</span>
//             </div>
//             <div className={styles.filterGroup}>
//               <label>Cuisine</label>
//               <select
//                 value={filters.cuisine}
//                 onChange={(e) => setFilters({ ...filters, cuisine: e.target.value })}
//               >
//                 <option value="all">All Cuisines</option>
//                 <option value="italian">Italian</option>
//                 <option value="asian">Asian</option>
//                 <option value="mexican">Mexican</option>
//               </select>
//             </div>
//             <div className={styles.filterGroup}>
//               <label>Ingredients</label>
//               <input
//                 type="text"
//                 placeholder="Enter ingredients separated by commas"
//                 value={filters.ingredients}
//                 onChange={(e) => setFilters({
//                   ...filters,
//                   ingredients: e.target.value.split(',').map(ingredient => ingredient.trim())
//                 })}
//               />
//               <span>Ingredients: {filters.ingredients.join(', ')}</span>
//             </div>
//             <button onClick={handleSubmit}>Submit</button>
//           </div>

//           <div className={styles.recipeGrid}>
//             {recommendations.length > 0 ? (
//               recommendations.map((recipe, index) => (
//                 <div
//                   key={index}
//                   className={styles.recipeCard}
//                   onClick={() => handleRecipeClick(recipe)}
//                   style={{ cursor: 'pointer' }}
//                 >
//                   <div className={styles.recipeDetails}>
//                     <h3>{recipe.name}</h3>
//                     <p>Cooking time: {recipe.cookingTime}</p>
//                     <h4>Ingredients:</h4>
//                     <ul>
//                       {recipe.ingredients.map((ingredient, idx) => (
//                         <li key={idx}>• {ingredient}</li>
//                       ))}
//                     </ul>
//                     <p>Calories: {recipe.calories}</p>
//                   </div>
//                 </div>
//               ))
//             ) : (
//               <p className={styles.whiteText}>No recommendations found. Try adjusting the filters and clicking Submit.</p>
//             )}
//           </div>
//         </div>

//         <div className={styles.chatbotSection}>
//           <div className={styles.chatHistory}>
//             {chatHistory.map((message, index) => (
//               <div key={index} className={styles.chatMessage}>
//                 <strong>{message.sender}:</strong> {message.text}
//               </div>
//             ))}
//           </div>
//           <div className={styles.chatInput}>
//             <input
//               type="text"
//               placeholder="Ask about recipes or cooking tips..."
//               value={chatMessage}
//               onChange={(e) => setChatMessage(e.target.value)}
//               onKeyDown={(e) => e.key === 'Enter' && handleSendChat()}
//             />
//             <button onClick={handleSendChat}>Send</button>
//           </div>
//         </div>
//       </main>
//     </div>
//   );
// };

// export default PrepPal;
