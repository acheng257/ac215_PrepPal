'use client';

import Hero from '@/components/home/Hero';
import WhatIs from '@/components/home/WhatIs';
import SignUp from '@/components/home/Signup'
import Login from '@/components/home/Login'
import Pantry from '@/components/home/Pantry'
import Recipe from '@/components/home/Recipe'
import PrepPal from '@/components/home/PrepPal';

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import React from 'react';

export default function Home() {
    // return (
        // <>
        //     <Hero />
        //     <WhatIs></WhatIs>
        //     <Login />
        //     <Pantry />
        //     <Recipe />
        //     <PrepPal />
        //     <Newsletters />
        //     <About />
        // </>
    // )
    return (
        <Router>
            <Routes>
            <Route path="/" element={
                <>
                    <Hero />
                    <WhatIs></WhatIs>
                    {/* <Login />
                    <Pantry />
                    <Recipe />
                    <PrepPal />
                    <Newsletters />
                    <About /> */}
                </>
            } />
            <Route path="/what-is" element={<WhatIs />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/pantry" element={<Pantry />} />
            <Route path="/recipe" element={<Recipe />} />
            <Route path="/preppal" element={<PrepPal />} />
            {/* <Route path="/newsletters" element={<Newsletters />} /> */}
            {/* <Route path="/about" element={<About />} /> */}
            {/* <Route path="/podcasts" element={<Podcasts />} /> */}
            </Routes>
        </Router>
        );
}