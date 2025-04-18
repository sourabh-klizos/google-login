// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
// import './App.css'
// import axios from 'axios';
// function App() {
  
//   const [loginUrl, setLoginUrl] = useState(null)

//   // const handleGoogleLogin = async () => {
//   //   const res = await fetch("http://localhost:8000/auth/google/login");
//   //   const login_url  = await res.json();
//   //   console.log(login_url)
//   //   window.location.href = login_url;
  

//   //   console.log(login_url)
    
//   // };

//   const handleGoogleLogin = () => {
//     window.location.href = "http://localhost:8000/auth/google/login";
//   };


//   return (
//     <>
//       <div className="App">
//       <button onClick={handleGoogleLogin}>
//         Login with Google
//       </button>
//     </div>
//     </>
//   )
// }

// export default App




import { useState } from 'react'
import './App.css'

function App() {

  const handleGoogleLogin = () => {
    window.location.href = "http://localhost:8000/auth/google/login";
  };

  const handleLinkedInLogin = () => {
    window.location.href = "http://localhost:8000/auth/linkedin";
  };

  const buttonStyle = {
    padding: '12px 20px',
    fontSize: '16px',
    borderRadius: '8px',
    border: 'none',
    cursor: 'pointer',
    color: '#fff',
    display: 'inline-flex',
    alignItems: 'center',
    margin: '10px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    transition: 'transform 0.2s',
  };

  const googleStyle = {
    ...buttonStyle,
    backgroundColor: '#212121',
  };

  const linkedinStyle = {
    ...buttonStyle,
    backgroundColor: '#0077B5',
  };

  return (
    <div className="App">
      <button onClick={handleGoogleLogin} style={googleStyle}>
        <img src="https://img.icons8.com/?size=100&id=V5cGWnc9R4xj&format=png&color=000000" alt="Google" style={{ width: 20, marginRight: 10 }} />
        Login with Google
      </button>

      <button onClick={handleLinkedInLogin} style={linkedinStyle}>
        <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" alt="LinkedIn" style={{ width: 20, marginRight: 10 }} />
        Login with LinkedIn
      </button>
    </div>
  )
}

export default App
