// 'use client';

// import React, { useState } from 'react';
// import styles from './styles.module.css';
// import { useRouter } from 'next/navigation';
// // import { Link } from 'react-router-dom';
// import Header from '@/components/layout/Header';
// import Link from 'next/link';

// const Login = () => {
//   const [email, setEmail] = useState('');
//   const [password, setPassword] = useState('');
//   const router = useRouter()

//   const handleSubmit = (event) => {
//     event.preventDefault();
    
//     // TODO: Add login logic, e.g., API request to validate user credentials
//     alert("Form submitted successfully!");
//     window.location.assign('index.html');
//   };

//   return (
//     <div className={styles.appContainer}>
//       <Header />
      
//       <div className={styles.container}>
//         <h2 className={styles.title}>Log In</h2>
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
//           <button type="submit" className={styles.submitButton}>Log In</button>
//         </form>
//         <p className={styles.footerText}>
//           Don't have an account?{' '}
//           {/* <a href="Signup.jsx" className={styles.loginLink}>Sign Up</a> */}
//           {/* <Link to="/signup">Sign Up</Link> */}
//           <Link href="/signup" className={styles.loginLink}>Sign Up</Link>
//         </p>
//       </div>
//     </div>
//   );
// };

// export default Login;

'use client';

import React, { useState } from 'react';
import styles from './styles.module.css';
import { useRouter } from 'next/navigation';
import Header from '@/components/layout/Header';
import Link from 'next/link';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    try {
      const response = await fetch('http://localhost:9000/test', {
        method: 'POST', // Assuming /test requires a POST request for login; change to 'GET' if necessary
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }), // Send credentials if necessary
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Response from backend:', data);
        // Navigate to the home page or another page after successful login
        router.push('/preppal'); // Change '/' to the desired route if needed
      } else {
        console.error('Failed to log in');
        alert('Login failed. Please check your credentials.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred. Please try again later.');
    }
  };

  return (
    <div className={styles.appContainer}>
      <Header />
      
      <div className={styles.container}>
        <h2 className={styles.title}>Log In</h2>
        <form className={styles.form} onSubmit={handleSubmit}>
          <div>
            <input
              type="email"
              placeholder="Email"
              className={styles.inputField}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div>
            <input
              type="password"
              placeholder="Password"
              className={styles.inputField}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className={styles.submitButton}>Log In</button>
        </form>
        <p className={styles.footerText}>
          Don't have an account?{' '}
          <Link href="/signup" className={styles.loginLink}>Sign Up</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;

