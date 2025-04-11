import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import axios from 'axios';
function App() {
  
  const [loginUrl, setLoginUrl] = useState(null)

  // const handleGoogleLogin = async () => {
  //   const res = await fetch("http://localhost:8000/auth/google/login");
  //   const login_url  = await res.json();
  //   console.log(login_url)
  //   window.location.href = login_url;
  

  //   console.log(login_url)
    
  // };

  const handleGoogleLogin = () => {
    window.location.href = "http://localhost:8000/auth/google/login";
  };


  return (
    <>
      <div className="App">
      <button onClick={handleGoogleLogin}>
        Login with Google
      </button>
    </div>
    </>
  )
}

export default App
