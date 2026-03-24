import React from 'react';
import LandingHero from './components/LandingHero';
import PricingSection from './components/PricingSection';
import OnboardingPreview from './components/OnboardingPreview';

export default function App() {
  return (
    <main>
      <LandingHero />
      <PricingSection />
      <OnboardingPreview />
    </main>
  );
}
