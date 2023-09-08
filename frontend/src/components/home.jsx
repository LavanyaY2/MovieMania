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
import TextField from '@mui/material/TextField';
import Moviecard from './moviecard';

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


function Home(props){

    const location = useLocation();
    const username = location.state?.username;
    const userId = location.state?.userId;
    const password = location.state?.password;

    const navigate = useNavigate();

    function rateMovies(){
        navigate('/rate', {
            state: {
              username: username,
              userId: userId,
              password: password
            },
          });
    }

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

    const [movieRecs, setMovieRecs] = useState([]);
    
    async function getMovieRecs(){
        let response = await client.get('/user/rec', {
            params: {
            user_id: userId,
            }
        });
        response = response.data;
        setMovieRecs(response);
    }
    
    const fetchMoviesRec = async (title, year) => {

        //get all the results
        const response = await fetch(`${API_URL}&s=${title}`);
        const movieData = await response.json();
        const allMovies = movieData.Search;

        const result = allMovies.filter((movie) => {
            const movieYear = movie.Year;
            // Compare the extracted year with the specified year
            return movieYear === year;
        })

        const firstMovie = result[0];
        return firstMovie;
    }


    const fetchRecMovies = async () => {
        await getMovieRecs();
        
        console.log("movie recs");
        console.log(movieRecs);

        // Use Promise.all to fetch movies for all recommended titles concurrently
        const movieResults = Object.keys(movieRecs.recommended_movies).map((key) => {
            const cleanedTitle = key.replace(/\(\d{4}\)/g, '').trim();
            const yearPattern = /\((\d{4})\)/; // Regular expression to match the year in parentheses
            const match = key.match(yearPattern);
            const year = match ? match[1]: null;
            return fetchMoviesRec(cleanedTitle, year);
        });

        // Wait for all promises to resolve - meaning we have the results for each 
        // recommended movie
        Promise.all(movieResults)
            .then((results) => {
            // Filter out any null results (movies not found)
            const filteredResults = results.filter((result) => result !== null);

            // Update the state with the filtered results
            setMovies(filteredResults);
            });
    }

    const [movies, setMovies] = useState([]);
    const [search, setSearch ] = useState([])

    //creating a function to search movies
    const fetchMovies = async (title) => {
        const response = await fetch(`${API_URL}&s=${title}`);
        const movieData = await response.json();
        setMovies(movieData.Search);
    }
    
    useEffect(() => {
        //inside here, calling the function that will fetch the movies (i.e. searchMovies)
        getMovieRecs();
        fetchRecMovies();
    }, [])

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

            <Container component="main" maxWidth="sm">
                <Box sx={{
                    marginTop: 4,
                    display: 'flex',
                    flexDirection: 'row',
                    alignItems: 'center',
                }}>
                    <TextField fullWidth label="Search for movies..." id="fullWidth" 
                    value={search}
                    onChange={(e) => setSearch(e.target.value)} />
                    <Button
                        type="submit"
                        variant="contained"
                        sx={{ mt: 3, mb: 3, ml:3, height:50, whiteSpace: 'nowrap' }}
                        onClick={() => fetchMovies(search) }
                        >
                        Search
                        </Button>
                </Box>

            </Container>
            <Container component="main" maxWidth='xl' >
                <div className='movieContainer'>
                    <h3>Recommended for you</h3>
                    
                </div>
                <div className='movieContainer'>
                <Button
                    type="button"
                    maxWidth="lg"
                    variant="contained"
                    sx={{ mt: 3, mb: 3, height:45 }}
                    onClick={rateMovies}
                    >
                    Rate Movies
                </Button>
                    
                </div>               
                
                {
                    movies?.length > 0 ?
                    (
                        <div className='movieContainer'>
                            { movies.map((movie) => (
                                <Moviecard movie={movie} userId={userId} movieId={movie.id} />
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

export default Home;