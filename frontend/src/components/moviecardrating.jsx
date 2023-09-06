import React from "react";
import axios from 'axios';
import { useState, useEffect } from 'react';
import Card from '@mui/material/Card';
import CardMedia from '@mui/material/CardMedia';
import Rating from '@mui/material/Rating';
import Button from '@mui/material/Button';

// setting default axios variables to the csrf token
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

// client instance with the base url
const client = axios.create({
  baseURL : "http://127.0.0.1:8000"
});


function Moviecardrating({ movie, userId }){
    const [value, setValue] = React.useState(0);

    
  //create state for rating and movie
  const [ratingData, setRatingData] = useState({
    user: '',
    movie: '',
    rating: ''
    
  });

  // adding input data
  const submitRating=(e)=>{
    console.log("submit rating");
    setRatingData({
      ...ratingData,
      [e.target.name]: e.target.value
    });
  }

  const formSubmit=(e, movieId)=> {

    console.log("form submit");
    console.log(movieId);
    console.log(userId);

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

    return (
        <div>
        <Card sx={{ width: 200, maxWidth: 200, borderRadius: 4, mb: 3, mr: 3, maxHeight: 300 }}>
            <CardMedia
                component='img'
                height='300'
                image={movie.Poster !== 'N/A' ? movie.Poster : "https://via.placeholder.com/310x420"} 
                alt={movie.Title} />
        </Card>
        <p>{movie.title}</p>
        {/* <Rating
            name='rating'
            value={value}
            onChange={(event, newValue) => {
            setValue(newValue);
            }}
        /> */}
        <input type='number' onChange={submitRating} name='rating' className='form-control'></input>
        <div>
        <Button type="submit"
              variant="contained"
              sx={{ mb: 3, height:30, mt: 3 }}
              onClick={e => formSubmit(e, movie.id)}>
            Submit Rating
        </Button>
        </div>
        </div> 
        
    );
}

export default Moviecardrating;


