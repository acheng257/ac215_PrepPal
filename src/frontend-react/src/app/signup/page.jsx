// 'use client';

// import React, { useState } from 'react';
// import styles from './styles.module.css';
// import Link from 'next/link'
// import Header from '@/components/layout/Header'
// import { useRouter } from 'next/navigation';

// const SignUp = () => {
//   const [email, setEmail] = useState('');
//   const [password, setPassword] = useState('');
//   const [confirmPassword, setConfirmPassword] = useState('');
//   const router = useRouter();

//   const handleSubmit = async (event) => {
//     event.preventDefault();
//     const apiUrl = 'http://localhost:9000';

//     if (password !== confirmPassword) {
//       alert("Passwords don't match!");
//       return;
//     }

//     try {
//       const formData = new FormData();
//       formData.append('username', email);
//       formData.append('password', password);

//       const response = await fetch(`${apiUrl}/auth/signup`, {
//         method: 'POST',
//         body: formData,
//       });

//       if (response.ok) {
//         const data = await response.json();
//         alert(data.message);
//         router.push('/preppal');
//       } else {
//         const errorData = await response.json();
//         alert(errorData.detail || 'Registration failed');
//       }
//     } catch (error) {
//       console.error('Error:', error);
//       alert('An error occurred. Please try again.');
//     }

//   };

//   return (
//     <div className={styles.appContainer}>
//       <Header />
//       <div className={styles.container}>
//         <h2 className={styles.title}>Sign Up</h2>
//         <form className={styles.form} onSubmit={handleSubmit}>
//           <div>
//             <input
//               type="email"
//               placeholder="Email"
//               className={styles.inputField}
//               value={email}
//               onChange={(e) => setEmail(e.target.value)}
//               required
//             />
//           </div>
//           <div>
//             <input
//               type="password"
//               placeholder="Password"
//               className={styles.inputField}
//               value={password}
//               onChange={(e) => setPassword(e.target.value)}
//               required
//             />
//           </div>
//           <div>
//             <input
//               type="password"
//               placeholder="Confirm Password"
//               className={styles.inputField}
//               value={confirmPassword}
//               onChange={(e) => setConfirmPassword(e.target.value)}
//               required
//             />
//           </div>
//           <button type="submit" className={styles.submitButton}>Sign Up</button>
//         </form>
//         <p className={styles.footerText}>
//           Already have an account?{' '}
//           <Link href="/login" className={styles.loginLink}>Log In</Link>
//         </p>
//       </div>
//     </div>
//   );
// };

// export default SignUp;

'use client';

import React, { useState } from 'react';
import styles from './styles.module.css';
import Link from 'next/link';
import Header from '@/components/layout/Header';
import { useRouter } from 'next/navigation';

const SignUp = () => {
  // State variables for all form fields
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [username, setUsername] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const router = useRouter();

  const handleSubmit = async (event) => {
    event.preventDefault();
    const apiUrl = 'http://localhost:9000';

    // Frontend validation for password confirmation
    if (password !== confirmPassword) {
      alert("Passwords don't match!");
      return;
    }

    try {
      // Create a new FormData object and append necessary fields
      const formData = new FormData();
      formData.append('first_name', firstName);
      formData.append('last_name', lastName);
      formData.append('username', username);
      formData.append('phone_number', phoneNumber);
      formData.append('password', password);

      // Send POST request to the signup endpoint
      const response = await fetch(`${apiUrl}/auth/signup`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        console.log("response ok");
        localStorage.setItem("userId", data.user_id);
        alert(data.message);
        router.push('/preppal'); // Redirect to the main page upon successful signup
      } else {
        const errorData = await response.json();
        alert(errorData.detail || 'Registration failed');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred. Please try again.');
    }
  };

  return (
    <div className={styles.appContainer}>
      <Header />
      <div className={styles.container}>
        <h2 className={styles.title}>Sign Up</h2>
        <form className={styles.form} onSubmit={handleSubmit}>
          {/* First Name Field */}
          <div>
            <input
              type="text"
              placeholder="First Name"
              className={styles.inputField}
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              required
            />
          </div>

          {/* Last Name Field */}
          <div>
            <input
              type="text"
              placeholder="Last Name"
              className={styles.inputField}
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              required
            />
          </div>

          {/* Username Field */}
          <div>
            <input
              type="text"
              placeholder="Username"
              className={styles.inputField}
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          {/* Phone Number Field */}
          <div>
            <input
              type="tel"
              placeholder="Phone Number"
              className={styles.inputField}
              value={phoneNumber}
              onChange={(e) => setPhoneNumber(e.target.value)}
              required
              pattern="^\+?1?\d{9,15}$" // Basic pattern for phone numbers
              title="Enter a valid phone number (e.g., +12345678901)"
            />
          </div>

          {/* Password Field */}
          <div>
            <input
              type="password"
              placeholder="Password"
              className={styles.inputField}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={8} // Enforce minimum password length
              title="Password must be at least 8 characters long"
            />
          </div>

          {/* Confirm Password Field */}
          <div>
            <input
              type="password"
              placeholder="Confirm Password"
              className={styles.inputField}
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              minLength={8}
            />
          </div>

          {/* Submit Button */}
          <button type="submit" className={styles.submitButton}>
            Sign Up
          </button>
        </form>

        {/* Link to Login Page */}
        <p className={styles.footerText}>
          Already have an account?{' '}
          <Link href="/login" className={styles.loginLink}>
            Log In
          </Link>
        </p>
      </div>
    </div>
  );
};

export default SignUp;
