import * as React from 'react';

import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

// setting default axios variables to the csrf token
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

// client instance with the base url
const client = axios.create({
    baseURL : "http://127.0.0.1:8000"
  });

const customTheme = createTheme({
    palette: {
      primary: {
        main: '#154f30', // Your desired primary color
      },
      secondary: {
        main: '#06170e', // Your desired secondary color
      },
      // You can define other colors like error, warning, info, and success here
    },
  });

function Login() {

    const [currentUser, setCurrentUser] = useState();
    const [username, setUsername] = useState();
    const [password, setPassword] = useState();
    const navigate = useNavigate();

    
    // login handler - sends login data to the django api
    function submitLogin(e){
      e.preventDefault();

      client.post(
        "/user/login",
        {
          username: username,
          password: password
        }
      )
      setCurrentUser(true);
    }

    useEffect(() => {
      if (currentUser){
        getUserDetails();
      }
    }, [currentUser]);
  
    // to set userId
    async function getUserDetails(){
      let response = await client.get('/user/users');
      response = response.data;
      response = response.find(user => user.username === username);

      navigate('/home', {
        state: {
          username: username,
          userId: response.id,
          password: password
        },
      });
    }

    
  return (
    <ThemeProvider theme={customTheme}>
      
      <Container component="main" maxWidth="xs">
        <Box
          sx={{
            marginTop: 30,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Typography component="h1" variant="h5">
            Login to elevate your experience!
          </Typography>
          <Box component="form" noValidate onSubmit={e => submitLogin(e)} sx={{ mt: 3 }}>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={12}>
                <TextField
                  name="username"
                  required
                  fullWidth
                  id="username"
                  label="Username"
                  autoFocus
                  value={username} 
                  onChange={e => setUsername(e.target.value)}
                />
              </Grid>
              <Grid item xs={12}>
              <TextField
                  required
                  fullWidth
                  name="password"
                  label="Password"
                  type="password"
                  id="password"
                  value={password} 
                  onChange={e => setPassword(e.target.value)}
                />
              </Grid>
            </Grid>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 3, height:45 }}
            >
              Log in
            </Button>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
  
}


export default Login;