import Image from 'next/image';
import styles from './WhatIs.module.css';

export default function WhatIs() {
    return (
        <section className={styles.section}>
            <h2 className={styles.title}>Welcome to PrepPal!</h2>
            <div className={styles.underline}></div>

            <div className={styles.content}>
                <div className={styles.textContent}>
                    <h3 className={styles.subtitle}>Personalized Meal Recommendations</h3>

                    <p>
                        After a long day of work, the last thing you want is to spend hours perusing over hundreds of recipes trying
                        to figure out what to cook for dinner. PrepPal is an <strong>LLM-powered</strong> application that considers
                        user taste profiles to recommend new, exciting recipes. You can interact with our chatbot to further customize
                        the recommendations or ask more specific questions about recipes.
                    </p>

                    <h3 className={styles.subtitle}>Reducing Food Waste</h3>

                    <p>
                        Although many recipe recommendation systems exist, we take a unique angle on it by prioritizing food waste reduction.
                        PrepPal prioritizes recommending recipes that use up more of the ingredients that a user already has, ensuring that
                        ingredients are used up before going bad and also offering more convenience to the user as they do not have to
                        go out to buy as many ingredients that they might only use once.
                    </p>

                    <p>
                        Our virtual pantry management system makes it easy for users to keep track of the ingredients in their pantry and also
                        helps inform our recommendation system. Simply enter the ingredients and quantities on our website when you get new
                        ingredients, and our system will automatically remove the ingredients that are used up in recipes you cook.
                    </p>

                </div>

                {/* <div className={styles.imageContainer}>
                    <Image
                        src="/assets/cheese-platter.png"
                        alt="Cheese platter with various types of cheese"
                        fill
                        sizes="(max-width: 768px) 100vw, 400px"
                        style={{
                            objectFit: 'cover',
                        }}
                        priority
                    />
                </div> */}
            </div>
        </section>
    );
}
