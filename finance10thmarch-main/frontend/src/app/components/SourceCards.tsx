'use client';

import { useState } from 'react';

interface Source {
  title?: string;
  url?: string;
  favicon?: string;
}

interface SourceCardsProps {
  sources: Source[];
}

// Function to extract domain from URL
const extractDomain = (url: string): string => {
  try {
    const domain = new URL(url).hostname.replace('www.', '');
    return domain.split('.')[0]; // Get the first part of the domain
  } catch {
    return 'source';
  }
};

// Function to get favicon URL
const getFaviconUrl = (url: string): string => {
  try {
    const domain = new URL(url).origin;
    return `https://www.google.com/s2/favicons?domain=${domain}&sz=64`;
  } catch {
    return '';
  }
};

export default function SourceCards({ sources }: SourceCardsProps) {
  const [expanded, setExpanded] = useState(false);
  
  // Display only first 3 sources by default, show all when expanded
  const visibleSources = expanded ? sources : sources.slice(0, 3);
  const hiddenCount = sources.length - visibleSources.length;

  if (!sources || sources.length === 0) {
    return null;
  }

  return (
    <div className="mb-2">
      <div className="flex items-center justify-between mb-1">
        <div className="flex items-center">
          <svg className="w-3.5 h-3.5 mr-1 text-slate-600 dark:text-slate-400" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M16 17L21 12L16 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M21 12H9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          <span className="text-xs font-medium text-slate-600 dark:text-slate-400">Pro</span>
        </div>
        <button 
          onClick={() => setExpanded(!expanded)} 
          className="text-xs text-slate-600 dark:text-slate-400 flex items-center"
        >
          {sources.length} sources
          <svg className={`w-3 h-3 ml-1 transition-transform ${expanded ? 'rotate-180' : ''}`} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M19 9L12 16L5 9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </div>
      
      <div className="flex flex-wrap gap-1.5">
        {visibleSources.map((source, index) => {
          const domain = source.url ? extractDomain(source.url) : 'source';
          const faviconUrl = source.url ? getFaviconUrl(source.url) : '';
          
          return (
            <a 
              key={index} 
              href={source.url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="bg-slate-100 dark:bg-slate-800/50 rounded-full py-1 px-2 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors flex items-center"
            >
              <div className="flex-shrink-0 w-4 h-4 rounded-full overflow-hidden bg-slate-200 dark:bg-slate-700 mr-1.5 flex items-center justify-center text-xs">
                {faviconUrl && (
                  <img 
                    src={faviconUrl} 
                    alt={domain} 
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      // If favicon fails to load, show the first letter of the domain
                      (e.target as HTMLImageElement).style.display = 'none';
                      (e.target as HTMLImageElement).parentElement!.innerHTML = domain.charAt(0).toUpperCase();
                    }}
                  />
                )}
              </div>
              <span className="text-xs font-medium text-slate-700 dark:text-slate-300 truncate">{domain}</span>
            </a>
          );
        })}
        
        {hiddenCount > 0 && (
          <button 
            onClick={() => setExpanded(true)}
            className="bg-slate-100 dark:bg-slate-800/50 rounded-full py-1 px-2 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
          >
            <span className="text-xs font-medium text-slate-600 dark:text-slate-400">+{hiddenCount}</span>
          </button>
        )}
      </div>
    </div>
  );
} 