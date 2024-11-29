'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import DataService from '@/services/DataService';

export default function Hero({ user, setUser }) {
    const router = useRouter();
    // const [user, setUser] = useState(DataService.GetUser());

    const handleLogout = () => {
        localStorage.removeItem('userId');
        setUser(null);
        router.push('/');
    };

    return (
        <section
            className="relative h-screen flex items-center justify-center text-center bg-black"
            style={{
                backgroundImage:
                    "linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('/assets/cooking.png')",
                backgroundSize: 'cover',
                backgroundPosition: 'center',
            }}
        >
            <div className="container mx-auto px-4 flex flex-col items-center">
                <h1 className="text-5xl md:text-7xl font-playfair text-white mb-6">
                    PrepPal
                </h1>
                <p className="text-xl md:text-2xl text-white mb-8">
                    Reducing Food Waste with Creative Recipes
                </p>
                {!user ? (
                    // user not logged in
                    <div className="flex space-x-4 justify-center">
                        <Link href="/login">
                            <button className="bg-white text-black font-semibold py-2 px-4 rounded hover:bg-gray-200">
                                Login
                            </button>
                        </Link>
                        <Link href="/signup">
                            <button className="bg-transparent border border-white text-white font-semibold py-2 px-4 rounded hover:bg-white hover:text-black">
                                Sign Up
                            </button>
                        </Link>
                    </div>
                ) : (
                    // user logged in
                    <div className="flex flex-col items-center space-y-4">
                        <p className="text-lg text-white">
                            Welcome back, {localStorage.getItem('userId')}!
                        </p>
                        <button
                            onClick={handleLogout}
                            className="bg-red-500 text-white font-semibold py-2 px-4 rounded hover:bg-red-600"
                        >
                            Logout
                        </button>
                    </div>
                )}
            </div>
        </section>
    );
}
