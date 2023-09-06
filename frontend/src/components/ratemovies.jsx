import * as React from 'react';
import axios from 'axios';
import { useState, useEffect } from 'react';
// router imports
import {useLocation, useNavigate} from 'react-router-dom';
import { createTheme, ThemeProvider } from '@mui/material/styles';

// general imports
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

//for the navbar
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Button from '@mui/material/Button';
import Moviecardrating from './moviecardrating';


// setting default axios variables to the csrf token
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

// client instance with the base url
const client = axios.create({
    baseURL : "http://127.0.0.1:8000"
});

// creating static variable
const API_URL = `${process.env.API_URL}`

const customTheme = createTheme({
    palette: {
      primary: {
        main: '#154f30', // Your desired primary color
      },
      secondary: {
        main: '#06170e', // Your desired secondary color
      },
    },
});


function Ratemovies(props){

    const [currentUser, setCurrentUser] = useState();

    // using the useEffect hook to determine if a user is logged in by
    // sending a get request to the user api endpoint
    useEffect(() => {
        client.get("/user/auth")
        .then(function(res){
        setCurrentUser(true);
        })
        .catch(function(error){
        setCurrentUser(false);
        })
    }, []);

    const navigate = useNavigate();
    
    // similar functionality for logout
    function submitLogout(e) {
        e.preventDefault();
        client.post(
        "/user/logout",
        {
            username: username,
            password: password,
            withCredentials: true
        }
        )
        navigate('/login');
    }

    useEffect(() => {
        //inside here, calling the function that will fetch the movies (i.e. searchMovies)
        viewMovies();
    }, [])

    // to get a list of movies - use to display all the movies
    const [movies, setMovies] = useState([]);
    async function viewMovies(){
        let response;
        client.get(
        "/user/movies?limit=10"
        ).then((res) => {
        response = res.data;
        console.log("movie response");
        console.log(res.data);

        setMovies(response);
        });
    }


    const location = useLocation();
    const username = location.state?.username;
    const userId = location.state?.userId;
    const password = location.state?.password;


    return (
        <ThemeProvider theme={customTheme}>
            <Box sx={{ flexGrow: 1}}>
                <AppBar position='static'>
                    <Toolbar>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        MovieMania
                    </Typography>
                    <Button color="inherit" onClick={(e) => {submitLogout(e)}}>
                        Log out
                    </Button>
                    </Toolbar>
                </AppBar>
            </Box>

            <Container component="main" maxWidth='xl'sx={{ mt:8 }} >
                {
                    movies?.length > 0 ?
                    (
                        <div className='movieContainer'>
                            { movies.map((movie) => (
                                <Moviecardrating movie={movie} userId={userId} />
                            )) }
                           
                        </div>
                    ) :
                    (
                        <div className='empty' >
                            <h1>No movies found</h1>
                        </div>
                    )
                }
            </Container>
        </ThemeProvider>
        
        
    );
};

export default Ratemovies;