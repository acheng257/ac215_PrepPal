'use client';

import { useState } from 'react';
import DataService from '@/services/DataService';

import Hero from '@/components/home/Hero';
import WhatIs from '@/components/home/WhatIs';

import React from 'react';

export default function Home() {
    const [user, setUser] = useState(DataService.GetUser());

    console.log("user is: ", user)
    return (
        <>
            {/* <Hero /> */}
            <Hero user={user} setUser={setUser} />
            <WhatIs></WhatIs>
        </>
    )
}
