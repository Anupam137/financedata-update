'use client';

import { useState, useEffect } from 'react';

interface SearchBarProps {
  query: string;
  setQuery: (query: string) => void;
  mode: string;
  setMode: (mode: string) => void;
  useStreaming: boolean;
  setUseStreaming: (useStreaming: boolean) => void;
  onSubmit: (event: React.FormEvent) => void;
  loading: boolean;
}

export default function SearchBar({
  query,
  setQuery,
  mode,
  setMode,
  useStreaming,
  setUseStreaming,
  onSubmit,
  loading
}: SearchBarProps) {
  const [showModeOptions, setShowModeOptions] = useState(false);
  const [currentPlaceholder, setCurrentPlaceholder] = useState('');
  const [isTyping, setIsTyping] = useState(true);
  const [currentExampleIndex, setCurrentExampleIndex] = useState(0);
  const [charIndex, setCharIndex] = useState(0);
  
  // Rotating placeholder examples
  const placeholderExamples = [
    "What's the latest market sentiment on NVIDIA?",
    "Is Tesla overvalued based on 2025 earnings?",
    "Compare Apple vs. Microsoft stock performance",
    "Backtest a 50-day moving average strategy on S&P 500",
    "Analyze social media sentiment for Bitcoin",
    "What are the top performing stocks in the energy sector?",
    "How will rising interest rates affect tech stocks?",
    "Show me insider trading activity for Amazon"
  ];
  
  // Typing animation effect
  useEffect(() => {
    const typingSpeed = 50; // milliseconds per character
    const pauseDuration = 2000; // pause at the end of typing
    const erasingSpeed = 30; // milliseconds per character when erasing
    
    let timer: NodeJS.Timeout;
    
    if (isTyping) {
      // Typing animation
      if (charIndex < placeholderExamples[currentExampleIndex].length) {
        timer = setTimeout(() => {
          setCurrentPlaceholder(placeholderExamples[currentExampleIndex].substring(0, charIndex + 1));
          setCharIndex(charIndex + 1);
        }, typingSpeed);
      } else {
        // Finished typing, pause before erasing
        timer = setTimeout(() => {
          setIsTyping(false);
        }, pauseDuration);
      }
    } else {
      // Erasing animation
      if (charIndex > 0) {
        timer = setTimeout(() => {
          setCurrentPlaceholder(placeholderExamples[currentExampleIndex].substring(0, charIndex - 1));
          setCharIndex(charIndex - 1);
        }, erasingSpeed);
      } else {
        // Finished erasing, move to next example
        setCurrentExampleIndex((currentExampleIndex + 1) % placeholderExamples.length);
        setIsTyping(true);
      }
    }
    
    return () => clearTimeout(timer);
  }, [charIndex, currentExampleIndex, isTyping, placeholderExamples]);
  
  // Shorter placeholder examples for mobile
  const getResponsivePlaceholder = () => {
    // On mobile, show a shorter version of the placeholder
    if (typeof window !== 'undefined' && window.innerWidth < 640) {
      const fullPlaceholder = placeholderExamples[currentExampleIndex].substring(0, charIndex);
      // Truncate to a reasonable length for mobile
      if (fullPlaceholder.length > 25) {
        return fullPlaceholder.substring(0, 25) + '...';
      }
      return fullPlaceholder;
    }
    return currentPlaceholder;
  };
  
  const handleModeChange = (newMode: string) => {
    setMode(newMode);
    setShowModeOptions(false);
  };
  
  return (
    <div className="w-full max-w-3xl mx-auto">
      <form onSubmit={onSubmit} className="relative">
        <div className="search-container glow-effect relative">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={getResponsivePlaceholder()}
            className="w-full px-4 py-3 md:px-6 md:py-4 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-full shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 text-slate-900 dark:text-slate-100 text-sm md:text-base transition-all duration-300 pr-[120px] md:pr-[180px] truncate"
          />
          
          <div className="absolute right-2 top-1/2 transform -translate-y-1/2 flex space-x-1 md:space-x-2">
            <button
              type="button"
              onClick={() => setShowModeOptions(!showModeOptions)}
              className="px-2 py-1.5 md:px-3 md:py-2 bg-gradient-to-r from-blue-500 to-teal-500 hover:from-blue-600 hover:to-teal-600 text-white rounded-full text-xs md:text-sm font-medium flex items-center transition-all duration-300 shadow-md whitespace-nowrap"
            >
              {mode === 'sonar' && (
                <svg className="w-3 h-3 md:w-4 md:h-4 mr-1" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <path d="M12 12L16 10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <path d="M12 8V12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              )}
              {mode === 'deep_research' && (
                <svg className="w-3 h-3 md:w-4 md:h-4 mr-1" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M21 21L15 15M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <path d="M10 7V13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <path d="M7 10H13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              )}
              {mode === 'deepseek' && (
                <svg className="w-3 h-3 md:w-4 md:h-4 mr-1" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M2 3H8C9.06087 3 10.0783 3.42143 10.8284 4.17157C11.5786 4.92172 12 5.93913 12 7V21C12 20.2044 11.6839 19.4413 11.1213 18.8787C10.5587 18.3161 9.79565 18 9 18H2V3Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <path d="M22 3H16C14.9391 3 13.9217 3.42143 13.1716 4.17157C12.4214 4.92172 12 5.93913 12 7V21C12 20.2044 12.3161 19.4413 12.8787 18.8787C13.4413 18.3161 14.2044 18 15 18H22V3Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              )}
              <span>
                {mode === 'sonar' && 'Pro Search'}
                {mode === 'deep_research' && 'Deep'}
                {mode === 'deepseek' && 'Pro'}
              </span>
              <svg className="w-3 h-3 md:w-4 md:h-4 ml-1" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M6 9L12 15L18 9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
            
            <button
              type="submit"
              disabled={loading}
              className="px-2 py-1.5 md:px-3 md:py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-full transition-all duration-300 disabled:bg-blue-400 flex items-center justify-center shadow-md min-w-[32px] md:min-w-[40px]"
            >
              {loading ? (
                <svg className="animate-spin h-3.5 w-3.5 md:h-4 md:w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              ) : (
                <svg className="w-3.5 h-3.5 md:w-4 md:h-4" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M21 21L15 15M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              )}
            </button>
          </div>
        </div>
        
        {/* Enhanced mode selection dropdown */}
        {showModeOptions && (
          <div className="absolute mt-2 w-64 right-0 md:right-[100px] bg-white dark:bg-slate-800 rounded-xl shadow-xl border border-slate-200 dark:border-slate-700 z-10 overflow-hidden animate-fadeIn">
            <div className="p-3">
              <button
                type="button"
                onClick={() => handleModeChange('sonar')}
                className={`w-full text-left px-3 py-2.5 rounded-lg flex items-center ${
                  mode === 'sonar' ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400' : 'hover:bg-slate-100 dark:hover:bg-slate-700'
                }`}
              >
                <div className="w-8 h-8 md:w-10 md:h-10 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center text-blue-600 dark:text-blue-400 mr-2 md:mr-3">
                  <svg className="w-4 h-4 md:w-5 md:h-5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M12 12L16 10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M12 8V12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </div>
                <div>
                  <div className="font-medium text-sm md:text-base">Pro Search</div>
                  <div className="text-xs text-slate-500 dark:text-slate-400">Quick answers for basic queries</div>
                </div>
              </button>
              
              <button
                type="button"
                onClick={() => handleModeChange('deep_research')}
                className={`w-full text-left px-3 py-2.5 rounded-lg flex items-center mt-2 ${
                  mode === 'deep_research' ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400' : 'hover:bg-slate-100 dark:hover:bg-slate-700'
                }`}
              >
                <div className="w-8 h-8 md:w-10 md:h-10 rounded-full bg-purple-100 dark:bg-purple-900 flex items-center justify-center text-purple-600 dark:text-purple-400 mr-2 md:mr-3">
                  <svg className="w-4 h-4 md:w-5 md:h-5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M21 21L15 15M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M10 7V13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M7 10H13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </div>
                <div>
                  <div className="font-medium text-sm md:text-base">Deep Research</div>
                  <div className="text-xs text-slate-500 dark:text-slate-400">Detailed analysis with comparisons</div>
                </div>
              </button>
              
              <button
                type="button"
                onClick={() => handleModeChange('deepseek')}
                className={`w-full text-left px-3 py-2.5 rounded-lg flex items-center mt-2 ${
                  mode === 'deepseek' ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400' : 'hover:bg-slate-100 dark:hover:bg-slate-700'
                }`}
              >
                <div className="w-8 h-8 md:w-10 md:h-10 rounded-full bg-teal-100 dark:bg-teal-900 flex items-center justify-center text-teal-600 dark:text-teal-400 mr-2 md:mr-3">
                  <svg className="w-4 h-4 md:w-5 md:h-5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M2 3H8C9.06087 3 10.0783 3.42143 10.8284 4.17157C11.5786 4.92172 12 5.93913 12 7V21C12 20.2044 11.6839 19.4413 11.1213 18.8787C10.5587 18.3161 9.79565 18 9 18H2V3Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M22 3H16C14.9391 3 13.9217 3.42143 13.1716 4.17157C12.4214 4.92172 12 5.93913 12 7V21C12 20.2044 12.3161 19.4413 12.8787 18.8787C13.4413 18.3161 14.2044 18 15 18H22V3Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </div>
                <div>
                  <div className="font-medium text-sm md:text-base">Comprehensive Research</div>
                  <div className="text-xs text-slate-500 dark:text-slate-400">Professional-grade financial analysis</div>
                </div>
              </button>
              
              <div className="mt-3 pt-3 border-t border-slate-200 dark:border-slate-700">
                <label className="flex items-center px-3 py-2 text-xs md:text-sm">
                  <input
                    type="checkbox"
                    checked={useStreaming}
                    onChange={() => setUseStreaming(!useStreaming)}
                    className="rounded border-slate-300 text-blue-600 focus:ring-blue-500 h-3 w-3 md:h-4 md:w-4 mr-2"
                  />
                  Enable streaming responses
                </label>
              </div>
            </div>
          </div>
        )}
      </form>
    </div>
  );
} 