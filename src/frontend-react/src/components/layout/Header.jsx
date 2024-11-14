'use client'

import { useState, useEffect } from 'react';
import { usePathname, useRouter } from 'next/navigation';
import { Home, Info, Podcasts, SmartToy, AccountCircle, LocalDining, BreakfastDining } from '@mui/icons-material';
import styles from './Header.module.css';

const navItems = [
    { name: 'Home', path: '/', sectionId: '', icon: <Home fontSize="small" /> },
    { name: 'My Pantry', path: '/pantry', sectionId: '', icon: <BreakfastDining fontSize="small" /> },
    { name: 'Recipes', path: '/preppal', sectionId: '', icon: <LocalDining fontSize="small" /> },
    { name: 'Chatbot', path: '/chat', sectionId: '', icon: <SmartToy fontSize="small" /> },
    { name: 'Username', path: '/', sectionId: '', icon: <AccountCircle fontSize="small" /> }
];

export default function Header() {
    const pathname = usePathname();
    const router = useRouter();
    const [isScrolled, setIsScrolled] = useState(false);
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

    useEffect(() => {
        if (typeof window !== 'undefined') {
            const handleScroll = () => {
                setIsScrolled(window.scrollY > 50);
            };
            window.addEventListener('scroll', handleScroll);
            return () => window.removeEventListener('scroll', handleScroll);
        }
    }, []);

    const handleNavigation = (item) => {
        if (item.path === '/') {
            if (pathname === '/') {
                // If already on the home page, force a full reload
                window.location.reload();
            } else {
                // Navigate to the home page if not currently on it
                router.replace('/');
            }
        } else {
            // Navigate to other pages like /pantry, /recipe, or /chat
            router.push(item.path);
        }
        // Close mobile menu after navigation
        setIsMobileMenuOpen(false);
    };

    return (
        // <header
        //     className={`fixed w-full top-0 z-50 transition-all duration-300 ${isScrolled ? 'bg-black/90' : 'bg-transparent'}`}
        // >
        <header
            className={`fixed w-full top-0 z-50 transition-all duration-300 ${isScrolled ? 'bg-black/90' : 'bg-transparent'
                }`}
        >
            <div className="container mx-auto px-4 h-20 flex items-center justify-between">
                <button
                    onClick={() => handleNavigation(navItems[0])} // Directly navigate to "Home"
                    className="text-white hover:text-white/90 transition-colors"
                >
                    <h1 className="text-2xl font-bold font-montserrat">PrepPal</h1>
                </button>

                {/* Desktop Navigation */}
                <div className={styles.navLinks}>
                    {navItems.map((item) => (
                        <button
                            key={item.name}
                            onClick={() => handleNavigation(item)}
                            className={`${styles.navLink} ${pathname === item.path ? styles.active : ''}`}
                        >
                            <span className={styles.icon}>{item.icon}</span>
                            <span className={styles.linkText}>{item.name}</span>
                        </button>
                    ))}
                </div>

                {/* Mobile Menu Button */}
                <button
                    className="md:hidden p-2"
                    onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                    aria-label="Toggle mobile menu"
                >
                    <div className={`w-6 h-0.5 bg-white mb-1.5 transition-all ${isMobileMenuOpen ? 'rotate-45 translate-y-2' : ''}`} />
                    <div className={`w-6 h-0.5 bg-white mb-1.5 ${isMobileMenuOpen ? 'opacity-0' : ''}`} />
                    <div className={`w-6 h-0.5 bg-white transition-all ${isMobileMenuOpen ? '-rotate-45 -translate-y-2' : ''}`} />
                </button>

                {/* Mobile Menu */}
                <div
                    className={`fixed md:hidden top-20 left-0 w-full bg-white shadow-lg transform transition-transform duration-300 ${
                        isMobileMenuOpen ? 'translate-y-0' : '-translate-y-full'
                    }`}
                >
                    <nav className="flex flex-col p-4">
                        {navItems.map((item) => (
                            <button
                                key={item.name}
                                onClick={() => handleNavigation(item)}
                                className="py-3 text-gray-800 border-b border-gray-200"
                            >
                                {item.name}
                            </button>
                        ))}
                    </nav>
                </div>
            </div>
        </header>
    );
}

