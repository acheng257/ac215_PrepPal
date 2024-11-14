// 'use client';

// import React, { useState } from 'react';
// import styles from './styles.module.css';
// import Header from '@/components/layout/Header';
// import Link from 'next/link';

// const PrepPal = () => {
//   const [filters, setFilters] = useState({
//     cookingTime: 30,
//     servings: 4,
//     cuisine: 'all',
//     ingredients: []
//   });
//   const [recommendations, setRecommendations] = useState([]);

//   const handleSubmit = async () => {
//     const apiUrl = 'http://localhost:9000/get_recs';

//     try {
//       const response = await fetch(apiUrl, {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ filters, more_recommendations: false }), // Adjust `more_recommendations` as needed
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


//               <Link href={`/recipe`} key={index} passHref>
//                 <div key={index} className={styles.recipeCard}>
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
//               </Link>
//               ))
//             ) : (
//               <p className={styles.whiteText}>No recommendations found. Try adjusting the filters and clicking Submit.</p>
//             )}
//           </div>
//         </div>

//         <div className={styles.chatbotSection}>
//           <div className={styles.chatHistory}>Chat history will appear here...</div>
//           <div className={styles.chatInput}>
//             <input type="text" placeholder="Ask about recipes or cooking tips..." />
//             <button>Send</button>
//           </div>
//         </div>
//       </main>
//     </div>
//   );
// };

// export default PrepPal;
'use client';

import React, { useState } from 'react';
import styles from './styles.module.css';
import Header from '@/components/layout/Header';
import { useRouter } from 'next/navigation';

const PrepPal = () => {
  const [filters, setFilters] = useState({
    cookingTime: 30,
    servings: 4,
    cuisine: 'all',
    ingredients: []
  });
  const [recommendations, setRecommendations] = useState([]);
  const router = useRouter();

  const handleSubmit = async () => {
    const apiUrl = 'http://localhost:9000/get_recs';

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ filters, more_recommendations: false }), // Adjust `more_recommendations` as needed
      });

      if (response.ok) {
        const data = await response.json();
        alert("Response ok");
        setRecommendations(data.recommendations);
      } else {
        const errorData = await response.json();
        alert(errorData.detail || 'Failed to fetch recommendations');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred. Please try again.');
    }
  };

  // Function to handle recipe card click and navigate to the /recipe page with recipe data
  // const handleRecipeClick = (recipe) => {
  //   console.log("recipe:", recipe);
  //   router.push({
  //     pathname: '/recipe',
  //     query: { data: JSON.stringify(recipe) } // Pass the entire recipe as a JSON string
  //   });
  // };
  // const handleRecipeClick = (recipe) => {
  //   router.push('/recipe', { query: JSON.stringify(recipe) });
  // };
  const handleRecipeClick = (recipe) => {
  
    // Manually construct the URL with query parameters
    const queryParams = new URLSearchParams({
      name: recipe.name,
      cookingTime: recipe.cookingTime,
      calories: recipe.calories,
      ingredients: JSON.stringify(recipe.ingredients), // Stringify array for URL compatibility
    });
  
    // Use router.push with the constructed URL
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
                  ingredients: e.target.value.split(',').map(ingredient => ingredient.trim())
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
          <div className={styles.chatHistory}>Chat history will appear here...</div>
          <div className={styles.chatInput}>
            <input type="text" placeholder="Ask about recipes or cooking tips..." />
            <button>Send</button>
          </div>
        </div>
      </main>
    </div>
  );
};

export default PrepPal;