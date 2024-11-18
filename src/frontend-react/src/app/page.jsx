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
    return (
        <>
            <Hero />
            <WhatIs></WhatIs>
        </>
    )
}
