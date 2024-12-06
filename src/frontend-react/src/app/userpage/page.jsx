'use client';

import React, { useState, useEffect, useRef } from 'react';
import styles from './styles.module.css';
import Header from '@/components/layout/Header';
import DataService from '@/services/DataService';
import { useRouter } from 'next/navigation';

const UserPage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [user, setUser] = useState(DataService.GetUser()); // Initialize as null
  const [favoriteRecipes, setFavoriteRecipes] = useState([]); // Array of detailed recipe objects
  const [loading, setLoading] = useState(true); // Loading state for favorite recipes
  const [fetchError, setFetchError] = useState(''); // Error state for fetching recipes
  const fileInputRef = useRef(null); // Ref for file input

  const router = useRouter();

  // Fetch user data inside useEffect
  useEffect(() => {
    const fetchUser = async () => {
      try {
        const currentUser = await DataService.GetUser();
        setUser(currentUser);
      } catch (error) {
        console.error('Error fetching user:', error);
        setFetchError('Failed to fetch user data.');
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  // Fetch favorite recipes when user is available
  useEffect(() => {
    const fetchFavoriteRecipes = async () => {
      if (!user) {
        setLoading(false);
        return;
      }

      try {
        // Fetch user preferences to get favorite recipe IDs
        const preferencesResponse = await DataService.GetUserPreferences(user);
        const recipeIds = preferencesResponse.data.favorite_recipes || [];

        console.log('Favorite recipe IDs:', recipeIds);

        if (recipeIds.length === 0) {
          setFavoriteRecipes([]);
          setLoading(false);
          return;
        }

        // Fetch detailed information for each recipe ID
        const recipePromises = recipeIds.map((id) => DataService.GetRecipeInfoById(id));
        const recipeResponses = await Promise.all(recipePromises);

        // Extract recipe objects from responses
        const recipes = recipeResponses.map((res) => res.data.recipe).filter(Boolean);

        console.log("favorite recipes are", recipes);

        setFavoriteRecipes(recipes);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching favorite recipes:', error);
        setFetchError('Failed to fetch favorite recipes.');
        setLoading(false);
      }
    };

    fetchFavoriteRecipes();
  }, [user]);

  const RecipeCard = ({ recipe, onClick }) => (
    <div className={styles.recipeCard} onClick={onClick}>
      <h3 className={styles.recipeName}>{recipe.title}</h3>
      <p className={styles.recipeDetails}>Cooking Time: {recipe.cooking_time} minutes</p>
      <p className={styles.recipeDetails}>Calories: {recipe.calories}</p>
      {/* Add more details as needed */}
    </div>
  );

  // Handle file selection
  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setUploadStatus('');
    setErrorMessage('');
  };

  // Handle form submission
  const handleFileUpload = async (e) => {
    e.preventDefault();

    if (!selectedFile) {
      setErrorMessage('Please select a file to upload.');
      return;
    }

    // Validate file type
    if (selectedFile.type !== 'text/plain') {
      setErrorMessage('Only text (.txt) files are allowed.');
      return;
    }

    // Validate file size (e.g., max 5MB)
    const maxSize = 5 * 1024 * 1024; // 5MB
    if (selectedFile.size > maxSize) {
      setErrorMessage('File size exceeds the 5MB limit.');
      return;
    }

    const formData = new FormData();
    formData.append('recipeFile', selectedFile);

    try {
      setUploadStatus('Uploading...');
      const response = await DataService.UploadRecipe(formData);

      if (response.data.success) {
        setUploadStatus('Upload successful!');
        // Clear the file input using ref
        setSelectedFile(null);
        if (fileInputRef.current) {
          fileInputRef.current.value = '';
        }

        // Optionally, refresh the favorite recipes if needed
        // For example, re-fetch user preferences and recipes
        // Here, we'll re-fetch favorite recipes by re-setting the user state
        setLoading(true);
        const refreshedUser = await DataService.GetUser();
        setUser(refreshedUser);
      } else {
        setUploadStatus('Upload failed. Please try again.');
        setErrorMessage(response.data.message || 'Unknown error.');
      }
    } catch (error) {
      console.error('Error uploading recipe:', error);
      setUploadStatus('An error occurred during upload.');
      setErrorMessage(error.response?.data?.message || 'Server error.');
    }
  };

  const handleRecipeClick = (recipe) => {
    const ingredients_list = recipe.ingredients.split('\n').map((ing) => ing.trim()).filter((ing) => ing.length > 0)
    const instructions_list = recipe.instructions.split('\n').map((ins) => ins.trim()).filter((ins) => ins.length > 0)
    const queryParams = new URLSearchParams({
      name: recipe.title,
      cookingTime: recipe.time,
      calories: recipe.calories,
      ingredients: JSON.stringify(ingredients_list),
      instructions: JSON.stringify(instructions_list),
    });
    router.push(`/recipe?${queryParams.toString()}`);
  };

  return (
    <div className={styles.appContainer}>
      <Header />
      <main className={styles.mainContent}>
        <section className={styles.favoriteRecipes}>
          <h2 className={styles.sectionTitle}>Your Favorite Recipes</h2>
          {loading ? (
            <p>Loading favorite recipes...</p>
          ) : fetchError ? (
            <p className={styles.errorMessage}>{fetchError}</p>
          ) : favoriteRecipes.length === 0 ? (
            <p>You have no favorite recipes.</p>
          ) : (
            <div className={styles.recipeGrid}>
              {favoriteRecipes.map((recipe) => (
                // Ensure recipe.recipe_id exists and is unique
                <RecipeCard key={recipe.recipe_id || recipe.id} recipe={recipe} onClick={() => handleRecipeClick(recipe)} />
              ))}
            </div>
          )}
        </section>
        <section className={styles.uploadSection}>
          <h2>Upload Your Own Recipe</h2>
          <form onSubmit={handleFileUpload} className={styles.uploadForm}>
            <input
              type="file"
              id="recipeFileInput"
              accept=".txt"
              onChange={handleFileChange}
              required
              className={styles.fileInput}
              ref={fileInputRef}
            />
            <button type="submit" className={styles.uploadButton}>
              Upload Recipe
            </button>
          </form>
          {uploadStatus && <p className={styles.statusMessage}>{uploadStatus}</p>}
          {errorMessage && <p className={styles.errorMessage}>{errorMessage}</p>}
        </section>
      </main>
    </div>
  );
};

export default UserPage;
