import Link from 'next/link';

export default function Hero() {
    return (
        <section
            className="relative h-screen flex items-center justify-center text-center bg-black"
            style={{
                backgroundImage: "linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('/assets/cooking.png')",
                backgroundSize: 'cover',
                backgroundPosition: 'center'
            }}
        >
            <div className="container mx-auto px-4 flex flex-col items-center">
                <h1 className="text-5xl md:text-7xl font-playfair text-white mb-6">
                    PrepPal
                </h1>
                <p className="text-xl md:text-2xl text-white mb-8">
                    Reducing Food Waste with Creative Recipes
                </p>
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
            </div>
        </section>
    )
}
