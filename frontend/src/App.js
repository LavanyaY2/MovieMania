import './App.css';
import React from 'react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import Container from 'react-bootstrap/Container';
// import Navbar from 'react-bootstrap/Navbar';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Login from './components/auth/login';
import Register from './components/auth/register';
import { useHistory } from 'react-router-dom';

//router imports
import {Routes, Route} from 'react-router-dom';
import Home from './components/home';
import Ratemovies from './components/ratemovies';

// setting default axios variables to the csrf token
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

// client instance with the base url
const client = axios.create({
  baseURL : "http://127.0.0.1:8000"
});


function App() {

  // app functional components - setting up some vars using useState
  const [currentUser, setCurrentUser] = useState();
  const [registrationToggle, setRegistrationToggle] = useState(false);
  const [username, setUsername] = useState();
  const [password, setPassword] = useState();
  const [rePassword, setRePassword] = useState('');


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

  //creating the toggle function
  function update_form_btn(){
    if (registrationToggle){
      document.getElementById("form btn").innerHTML = "Register";
      setRegistrationToggle(false);
    } else {
      document.getElementById("form btn").innerHTML = "Login";
      setRegistrationToggle(true);
    }
  }

  // creating handles to handle login, logout and register
  function submitRegistration(e){
    e.preventDefault(); // preventing default reloading of the page
    client.post(
      "/user/register",
      {
        username: username,
        password: password,
        re_password: rePassword
      }
    ).then(function(res){
      client.post(
        "/user/login",
        {
          username: username,
          password: password
        }
      ).then(function(res){
        setCurrentUser(true);
      })
    });
  }

  // login handler - sends login data to the django api
  function submitLogin(e){
    e.preventDefault();

    client.post(
      "/user/login",
      {
        username: username,
        password: password
      }
    ).then(function(res){
      setCurrentUser(true);
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
    ).then(function(res) {
      setCurrentUser(false);
    });
  }


  useEffect(() => {
    if (currentUser){
      getUserDetails();
    }
  }, [currentUser]);

  // to set userId
  const [userId, setUserId] = useState();
  async function getUserDetails(){
    if(currentUser){
      let response = await client.get('/user/users');
      response = response.data;
      response = response.find(user => user.username === username);
      setUserId(response.id);
    }
  }


  //create state for rating and movie
  const [ratingData, setRatingData] = useState({
    user: '',
    movie: '',
    rating: ''
    
  });

  // adding input data
  const submitRating=(e)=>{
    setRatingData({
      ...ratingData,
      [e.target.name]: e.target.value
    });
  }

  const formSubmit=(e, movieId)=> {

    e.preventDefault();

    try{
      client.post(
        "/user/rate",
        {
          user: userId,
          movie: movieId,
          rating: ratingData.rating
        }
        ,
        {
          headers: {
            "content-type": "application/json"
          }
        }
      );
    } catch(error){
      console.log(error);
    }
    
  }


  // to get a list of movies - use to display all the movies
  const [movies, setMovies] = useState([]);
  function viewMovies(e){
    e.preventDefault();

    let response;
    client.get(
      "/user/movies?limit=10"
    ).then((res) => {
      response = res.data;
      setMovies(response);
    });
  }


  // to view the submit rating form
  const [rate, setRate] = useState(false);
  function rateMovie(e){
    e.preventDefault();
    setRate(true);
  }


  //now we need to create a state for movie recs - we need to send in the user
  // id and 

  const [movieRecs, setMovieRecs] = useState([])

  function getMovieRecs(e){

    e.preventDefault();

    client.get('/user/rec', {
      params: {
        user_id: userId,
      }
    })
    .then((response) => {
      console.log(response.data);
    })
    .catch(error => {
      console.error(error);
    });

  }

  return (
    <div>
      <Routes>
        <Route path='/' element={<Register/>} />
        <Route path='/login' element={<Login/>} />
        <Route path='/home' element={<Home/>} />
        <Route path='/rate' element={<Ratemovies/>} />
      </Routes>
    </div>
  );
  
}

export default App;
