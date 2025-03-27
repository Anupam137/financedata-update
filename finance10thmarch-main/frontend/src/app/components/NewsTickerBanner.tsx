'use client';

import { useState, useEffect } from 'react';

// Sample news data
const newsItems = [
  {
    id: 1,
    title: "Fed signals potential rate cuts later this year",
    category: "Economy",
    isBreaking: true
  },
  {
    id: 2,
    title: "NVIDIA reports record quarterly earnings, stock surges",
    category: "Stocks",
    isBreaking: false
  },
  {
    id: 3,
    title: "Treasury yields fall as inflation data comes in below expectations",
    category: "Bonds",
    isBreaking: false
  },
  {
    id: 4,
    title: "Bitcoin breaks $70,000 mark for the first time",
    category: "Crypto",
    isBreaking: true
  },
  {
    id: 5,
    title: "Oil prices stabilize after OPEC+ production decision",
    category: "Commodities",
    isBreaking: false
  }
];

export default function NewsTickerBanner() {
  const [currentDate, setCurrentDate] = useState<string>('');
  
  // Format date in a consistent way that doesn't depend on locale
  useEffect(() => {
    const date = new Date();
    const day = date.getDate().toString().padStart(2, '0');
    const month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][date.getMonth()];
    const year = date.getFullYear();
    setCurrentDate(`${day} ${month} ${year}`);
  }, []);
  
  return (
    <div className="w-full bg-gradient-to-r from-blue-600 to-teal-600 text-white py-1.5 overflow-hidden">
      <div className="ticker-container">
        <div className="ticker-wrapper">
          {newsItems.map((item) => (
            <div key={item.id} className="ticker-item px-8">
              <div className="flex items-center">
                {item.isBreaking && (
                  <span className="bg-red-500 text-white text-xs px-1.5 py-0.5 rounded mr-2 font-medium">BREAKING</span>
                )}
                <span className="font-medium">{item.category}:</span>
                <span className="ml-1.5">{item.title}</span>
                <span className="hidden sm:inline mx-4 text-white/50">•</span>
                {/* Only render the date on the client side after it's been set */}
                {currentDate && (
                  <span className="hidden sm:inline text-white/70">{currentDate}</span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
} 