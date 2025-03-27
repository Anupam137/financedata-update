'use client';

import { useState } from 'react';

// Sample market data
const marketData = [
  {
    id: 'sp500',
    name: 'S&P 500',
    value: '5,021.84',
    change: '+0.57%',
    isUp: true,
    chart: [2780, 2790, 2810, 2805, 2830, 2845, 2860, 2865, 2870, 2880]
  },
  {
    id: 'nasdaq',
    name: 'NASDAQ',
    value: '15,990.66',
    change: '+0.95%',
    isUp: true,
    chart: [9180, 9220, 9250, 9270, 9300, 9320, 9350, 9370, 9390, 9400]
  },
  {
    id: 'dow',
    name: 'DOW',
    value: '38,773.12',
    change: '-0.12%',
    isUp: false,
    chart: [33450, 33480, 33520, 33510, 33490, 33470, 33450, 33430, 33420, 33400]
  },
  {
    id: 'btc',
    name: 'Bitcoin',
    value: '$68,234.51',
    change: '+2.34%',
    isUp: true,
    chart: [62100, 62500, 63200, 64000, 64800, 65200, 65800, 66500, 67200, 68200]
  },
  {
    id: 'eth',
    name: 'Ethereum',
    value: '$3,845.27',
    change: '+1.87%',
    isUp: true,
    chart: [3450, 3480, 3520, 3560, 3590, 3620, 3650, 3700, 3750, 3840]
  },
  {
    id: 'gold',
    name: 'Gold',
    value: '$2,175.30',
    change: '+0.32%',
    isUp: true,
    chart: [2120, 2125, 2130, 2135, 2140, 2145, 2150, 2160, 2165, 2175]
  }
];

// News headlines
const newsHeadlines = [
  {
    title: 'Fed signals potential rate cuts later this year',
    source: 'Financial Times',
    time: '2h ago'
  },
  {
    title: 'NVIDIA reports record quarterly earnings, stock surges',
    source: 'Bloomberg',
    time: '4h ago'
  },
  {
    title: 'Treasury yields fall as inflation data comes in below expectations',
    source: 'CNBC',
    time: '6h ago'
  }
];

export default function MarketSnapshot() {
  const [activeTab, setActiveTab] = useState('markets');
  
  // Function to render mini sparkline chart
  const renderSparkline = (data: number[], isUp: boolean) => {
    const min = Math.min(...data);
    const max = Math.max(...data);
    const range = max - min;
    
    const points = data.map((value, index) => {
      const x = (index / (data.length - 1)) * 100;
      const y = 100 - ((value - min) / range) * 100;
      return `${x},${y}`;
    }).join(' ');
    
    return (
      <svg className="w-14 h-6" viewBox="0 0 100 100" preserveAspectRatio="none">
        <polyline
          points={points}
          fill="none"
          stroke={isUp ? 'var(--secondary)' : 'var(--danger)'}
          strokeWidth="2"
        />
      </svg>
    );
  };
  
  return (
    <div className="w-full mb-4">
      {/* Tab navigation */}
      <div className="flex border-b border-slate-200 dark:border-slate-700 mb-3 overflow-x-auto scrollbar-hide">
        <button
          className={`px-3 py-1.5 font-medium text-xs whitespace-nowrap ${
            activeTab === 'markets'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
          }`}
          onClick={() => setActiveTab('markets')}
        >
          Markets
        </button>
        <button
          className={`px-3 py-1.5 font-medium text-xs whitespace-nowrap ${
            activeTab === 'news'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
          }`}
          onClick={() => setActiveTab('news')}
        >
          Latest News
        </button>
        <button
          className={`px-3 py-1.5 font-medium text-xs whitespace-nowrap ${
            activeTab === 'trending'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
          }`}
          onClick={() => setActiveTab('trending')}
        >
          Trending
        </button>
      </div>
      
      {/* Market cards */}
      {activeTab === 'markets' && (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-2">
          {marketData.map((item) => (
            <div
              key={item.id}
              className="bg-white dark:bg-slate-800 rounded-lg shadow-sm border border-slate-200 dark:border-slate-700 p-2 card-hover"
            >
              <div className="flex justify-between items-start mb-1">
                <h3 className="font-medium text-xs">{item.name}</h3>
                {renderSparkline(item.chart, item.isUp)}
              </div>
              <div className="font-mono text-sm font-semibold">{item.value}</div>
              <div className={`text-xs ${item.isUp ? 'market-up' : 'market-down'}`}>
                {item.change}
              </div>
            </div>
          ))}
        </div>
      )}
      
      {/* News headlines */}
      {activeTab === 'news' && (
        <div className="space-y-2">
          {newsHeadlines.map((news, index) => (
            <div key={index} className="bg-white dark:bg-slate-800 rounded-lg shadow-sm border border-slate-200 dark:border-slate-700 p-2.5 card-hover">
              <h3 className="font-medium mb-1 text-sm">{news.title}</h3>
              <div className="flex justify-between text-xs text-slate-500 dark:text-slate-400">
                <span>{news.source}</span>
                <span>{news.time}</span>
              </div>
            </div>
          ))}
        </div>
      )}
      
      {/* Trending searches */}
      {activeTab === 'trending' && (
        <div className="bg-white dark:bg-slate-800 rounded-lg shadow-sm border border-slate-200 dark:border-slate-700 p-3">
          <h3 className="font-medium mb-2 text-sm">Trending Searches</h3>
          <ol className="list-decimal list-inside space-y-1 text-sm">
            <li className="text-slate-700 dark:text-slate-300">NVDA stock analysis</li>
            <li className="text-slate-700 dark:text-slate-300">Bitcoin price prediction</li>
            <li className="text-slate-700 dark:text-slate-300">S&P 500 outlook</li>
            <li className="text-slate-700 dark:text-slate-300">Tesla earnings report</li>
            <li className="text-slate-700 dark:text-slate-300">Interest rate impact on markets</li>
          </ol>
        </div>
      )}
    </div>
  );
} 