import React from "react";
import axios from 'axios';
import { useState } from 'react';
import Card from '@mui/material/Card';
import CardMedia from '@mui/material/CardMedia';

// setting default axios variables to the csrf token
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

// client instance with the base url
const client = axios.create({
  baseURL : "http://127.0.0.1:8000"
});


function Moviecard({ movie, userId }){

    return (
        <div>
            <Card sx={{ width: 200, maxWidth: 200, borderRadius: 4, mb: 3, mr: 3, maxHeight: 300 }}>
                <CardMedia
                    component='img'
                    height='300'
                    image={movie.Poster !== 'N/A' ? movie.Poster : "https://via.placeholder.com/310x420"} 
                    alt={movie.Title} />
            </Card>
        </div>
       
    );
}

export default Moviecard;


