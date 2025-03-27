'use client';

import { useState, useEffect } from 'react';

// Sample sentiment data (will be replaced with API data later)
const sampleSentimentData = {
  lastUpdated: new Date().toISOString(),
  overallMarketSentiment: 'Cautiously Bullish',
  sentimentScore: 65, // 0-100 scale
  keyFactors: [
    { factor: 'Fed Policy', impact: 'Positive', description: 'Recent dovish comments suggest potential rate cuts' },
    { factor: 'Earnings Season', impact: 'Mixed', description: 'Tech outperforming, consumer staples underperforming' },
    { factor: 'Geopolitical', impact: 'Negative', description: 'Ongoing tensions creating market uncertainty' }
  ],
  sectorSentiment: [
    { sector: 'Technology', sentiment: 'Bullish', score: 78, change: 'up' },
    { sector: 'Healthcare', sentiment: 'Neutral', score: 52, change: 'down' },
    { sector: 'Energy', sentiment: 'Bearish', score: 35, change: 'down' },
    { sector: 'Financials', sentiment: 'Bullish', score: 72, change: 'up' },
    { sector: 'Consumer Cyclical', sentiment: 'Neutral', score: 50, change: 'up' }
  ],
  aiInsight: "Market participants are showing increased risk appetite despite mixed economic signals. The technology sector continues to lead market gains, driven by AI-related stocks. Watch for potential volatility around upcoming Fed announcements and Q2 earnings reports from major retailers."
};

export default function MarketSentimentPanel() {
  const [sentimentData] = useState(sampleSentimentData);
  const [timeAgo, setTimeAgo] = useState<string>('');
  const [isClient, setIsClient] = useState(false);
  
  // Set isClient to true when component mounts (client-side only)
  useEffect(() => {
    setIsClient(true);
  }, []);
  
  // Update the time display on the client side only
  useEffect(() => {
    if (!isClient) return;
    
    // Format the timestamp
    const formatTimeAgo = (dateString: string) => {
      const date = new Date(dateString);
      const now = new Date();
      const diffMs = now.getTime() - date.getTime();
      const diffMins = Math.round(diffMs / 60000);
      
      if (diffMins < 1) return 'Just now';
      if (diffMins < 60) return `${diffMins} min ago`;
      
      const diffHours = Math.floor(diffMins / 60);
      if (diffHours < 24) return `${diffHours} hr ago`;
      
      const diffDays = Math.floor(diffHours / 24);
      return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
    };

    setTimeAgo(formatTimeAgo(sentimentData.lastUpdated));

    // Set up an interval to update the time every minute
    const intervalId = setInterval(() => {
      setTimeAgo(formatTimeAgo(sentimentData.lastUpdated));
    }, 60000);

    return () => clearInterval(intervalId);
  }, [sentimentData.lastUpdated, isClient]);
  
  // Get color based on sentiment
  const getSentimentColor = (sentiment: string) => {
    switch (sentiment.toLowerCase()) {
      case 'bullish': return 'text-green-600 dark:text-green-400';
      case 'bearish': return 'text-red-600 dark:text-red-400';
      default: return 'text-amber-600 dark:text-amber-400';
    }
  };
  
  // Get color based on impact
  const getImpactColor = (impact: string) => {
    switch (impact.toLowerCase()) {
      case 'positive': return 'text-green-600 dark:text-green-400';
      case 'negative': return 'text-red-600 dark:text-red-400';
      default: return 'text-amber-600 dark:text-amber-400';
    }
  };
  
  // Get color based on change direction
  const getChangeColor = (change: string) => {
    return change === 'up' 
      ? 'text-green-600 dark:text-green-400' 
      : 'text-red-600 dark:text-red-400';
  };
  
  // Get icon based on change direction
  const getChangeIcon = (change: string) => {
    return change === 'up' 
      ? '↑' 
      : '↓';
  };
  
  return (
    <div className="bg-white dark:bg-slate-800 rounded-xl shadow-md overflow-hidden border border-slate-200 dark:border-slate-700">
      <div className="bg-gradient-to-r from-blue-600 to-teal-600 px-3 py-2 text-white">
        <div className="flex justify-between items-center">
          <h3 className="font-bold text-base flex items-center">
            <svg className="w-4 h-4 mr-1.5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" fill="currentColor" fillOpacity="0.2"/>
              <path d="M12 8V12L15 15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            AI Market Sentiment Analysis
          </h3>
          <div className="text-xs flex items-center">
            <span className="animate-pulse mr-1">●</span>
            {isClient ? (
              `Updated ${timeAgo}`
            ) : (
              "Updated"
            )}
          </div>
        </div>
      </div>
      
      <div className="p-3">
        <div className="grid grid-cols-12 gap-3">
          {/* Left column: Overall sentiment and key factors */}
          <div className="col-span-12 md:col-span-5">
            <div className="flex items-center mb-2">
              <div className="mr-3">
                <div className="text-xs text-slate-500 dark:text-slate-400">Overall Market</div>
                <div className="text-xl font-bold">{sentimentData.overallMarketSentiment}</div>
              </div>
              <div className="flex-1">
                <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2">
                  <div 
                    className="bg-gradient-to-r from-red-500 via-amber-500 to-green-500 h-2 rounded-full" 
                    style={{ width: `${sentimentData.sentimentScore}%` }}
                  ></div>
                </div>
              </div>
            </div>
            
            <div className="mt-3">
              <h4 className="text-xs font-medium mb-1.5 text-slate-500 dark:text-slate-400">Key Market Factors</h4>
              <div className="space-y-1.5">
                {sentimentData.keyFactors.map((factor, index) => (
                  <div key={index} className="flex items-start">
                    <div className={`px-1.5 py-0.5 rounded text-xs font-medium ${getImpactColor(factor.impact)} bg-opacity-10 dark:bg-opacity-20 bg-current`}>
                      {factor.impact}
                    </div>
                    <div className="ml-2">
                      <div className="font-medium text-xs">{factor.factor}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
          
          {/* Middle column: Sector sentiment */}
          <div className="col-span-12 md:col-span-3">
            <h4 className="text-xs font-medium mb-1.5 text-slate-500 dark:text-slate-400">Sector Sentiment</h4>
            <div className="space-y-1.5">
              {sentimentData.sectorSentiment.map((sector, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="w-1.5 h-1.5 rounded-full bg-current mr-1.5" style={{ 
                      color: sector.score > 65 ? '#10b981' : sector.score > 45 ? '#f59e0b' : '#ef4444'
                    }}></div>
                    <span className="text-xs">{sector.sector}</span>
                  </div>
                  <div className="flex items-center">
                    <span className={`text-xs font-medium ${getSentimentColor(sector.sentiment)}`}>
                      {sector.sentiment}
                    </span>
                    <span className={`ml-1 text-xs ${getChangeColor(sector.change)}`}>
                      {getChangeIcon(sector.change)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          {/* Right column: AI insight */}
          <div className="col-span-12 md:col-span-4">
            <div className="p-2 bg-slate-50 dark:bg-slate-700 rounded-lg border border-slate-200 dark:border-slate-600 h-full">
              <div className="text-xs font-medium mb-1">AI Market Insight</div>
              <p className="text-xs text-slate-600 dark:text-slate-300 line-clamp-5">{sentimentData.aiInsight}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 