// app/upload-recipe/page.jsx

'use client';

import React, { useState } from 'react';
import styles from './styles.module.css';
import Header from '@/components/layout/Header';
import DataService from '@/services/DataService';

const UserPage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

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
        // Optionally, clear the file input
        setSelectedFile(null);
        document.getElementById('recipeFileInput').value = '';
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

  return (
    <div className={styles.appContainer}>
      <Header />
      <main className={styles.mainContent}>
        <section className={styles.uploadSection}>
          <h2>Upload Your Recipe</h2>
          <form onSubmit={handleFileUpload} className={styles.uploadForm}>
            <input
              type="file"
              id="recipeFileInput"
              accept=".txt"
              onChange={handleFileChange}
              required
              className={styles.fileInput}
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
