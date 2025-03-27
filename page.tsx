'use client';

import { useState, useEffect, useRef } from 'react';
import Sidebar from './components/Sidebar';
import SearchBar from './components/SearchBar';
import MarketSnapshot from './components/MarketSnapshot';
import SearchResults from './components/SearchResults';
import ExampleQueries from './components/ExampleQueries';
import NewsTickerBanner from './components/NewsTickerBanner';
import MarketSentimentPanel from './components/MarketSentimentPanel';

interface Source {
  title?: string;
  url?: string;
}

interface SearchResult {
  answer: string;
  sources?: Source[];
  data?: Record<string, unknown>;
  session_id?: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export default function Home() {
  const [query, setQuery] = useState('');
  const [mode, setMode] = useState('sonar'); // 'sonar', 'deep_research', or 'deepseek'
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<{query: string, result: SearchResult}[]>([]);
  const [error, setError] = useState('');
  const [statusMessages, setStatusMessages] = useState<string[]>([]);
  const [useStreaming, setUseStreaming] = useState(true);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [showDeepResearchConfirm, setShowDeepResearchConfirm] = useState(false);
  const [showDeepSeekConfirm, setShowDeepSeekConfirm] = useState(false);
  const [isFollowUpQuestion, setIsFollowUpQuestion] = useState(false);
  
  const abortControllerRef = useRef<AbortController | null>(null);
  
  // Clean up any ongoing fetch when component unmounts
  useEffect(() => {
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, []);
  
  // Debug logging for session ID
  useEffect(() => {
    console.log('Session ID updated:', sessionId);
  }, [sessionId]);
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!query.trim()) {
      setError('Please enter a search query');
      return;
    }

    // Check if deep research mode is requested and needs confirmation
    if (mode === 'deep_research' && !showDeepResearchConfirm) {
      setShowDeepResearchConfirm(true);
      return;
    }

    // Check if deepseek mode is requested and needs confirmation
    if (mode === 'deepseek' && !showDeepSeekConfirm) {
      setShowDeepSeekConfirm(true);
      return;
    }

    // Reset confirmation states if proceeding
    if (showDeepResearchConfirm) {
      setShowDeepResearchConfirm(false);
    }
    
    if (showDeepSeekConfirm) {
      setShowDeepSeekConfirm(false);
    }
    
    setLoading(true);
    setError('');
    
    // Determine if this is a follow-up question
    // A follow-up question occurs when we already have results and a session ID
    const isFollowUp = results.length > 0 && sessionId !== null;
    setIsFollowUpQuestion(isFollowUp);
    
    console.log('Submitting query:', query);
    console.log('Is follow-up question:', isFollowUp);
    console.log('Current session ID:', sessionId);
    
    // Don't reset the result if it's a follow-up question
    // This helps maintain the conversation context in the UI
    if (!isFollowUp) {
      setResults([]);
    }
    
    setStatusMessages([]);
    
    // Abort any ongoing fetch
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    
    // Create a new AbortController
    abortControllerRef.current = new AbortController();
    
    // Prepare the request body with the current session ID
    const requestBody = {
      query,
      mode,
      session_id: sessionId
    };
    
    // Log the request for debugging
    console.log('Sending request with session ID:', sessionId);
    
    try {
      if (useStreaming) {
        // Streaming approach
        const response = await fetch(`${API_BASE_URL}/api/search/stream`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
          signal: abortControllerRef.current.signal,
        });
        
        const reader = response.body?.getReader();
        if (!reader) {
          throw new Error('Failed to get response reader');
        }
        
        const decoder = new TextDecoder();
        let buffer = '';
        
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          
          buffer += decoder.decode(value, { stream: true });
          
          // Process complete lines
          const lines = buffer.split('\n');
          buffer = lines.pop() || '';
          
          for (const line of lines) {
            if (!line.trim()) continue;
            
            // Check if this is a data line
            if (line.startsWith('data: ')) {
              try {
                // Remove the 'data: ' prefix and parse the JSON
                const jsonStr = line.slice(6);
                const data = JSON.parse(jsonStr);
                
                if (data.type === 'status') {
                  setStatusMessages(prev => [...prev, data.content]);
                  // Store session ID if provided
                  if (data.session_id && (!sessionId || sessionId !== data.session_id)) {
                    console.log('Updating session ID from status message:', data.session_id);
                    setSessionId(data.session_id);
                  }
                } else if (data.type === 'result') {
                  setResults(prev => [...prev, {
                    query: query,
                    result: {
                      answer: data.content,
                      sources: data.sources || [],
                      session_id: data.session_id
                    }
                  }]);
                  // Store session ID if provided
                  if (data.session_id) {
                    console.log('Updating session ID from result:', data.session_id);
                    setSessionId(data.session_id);
                  }
                  setLoading(false);
                } else if (data.type === 'error') {
                  setError(data.content);
                  // Store session ID if provided
                  if (data.session_id && (!sessionId || sessionId !== data.session_id)) {
                    console.log('Updating session ID from error message:', data.session_id);
                    setSessionId(data.session_id);
                  }
                  setLoading(false);
                }
              } catch (err) {
                console.error('Error parsing SSE data:', err, 'Line:', line);
              }
            }
          }
        }
      } else {
        // Non-streaming approach
        const response = await fetch(`${API_BASE_URL}/api/search`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
          signal: abortControllerRef.current.signal,
        });
        
        const data = await response.json();
        
        if (response.ok) {
          // Store session ID if provided
          if (data.session_id) {
            console.log('Updating session ID from response:', data.session_id);
            setSessionId(data.session_id);
          }
          
          setResults(prev => [...prev, {
            query: query,
            result: data
          }]);
        } else {
          setError(data.detail || 'An error occurred');
        }
        
        setLoading(false);
      }
    } catch (err) {
      if (err instanceof Error && err.name !== 'AbortError') {
        console.error('Error during search:', err);
        setError(`Error: ${err.message}`);
        setLoading(false);
      }
    }
  };
  
  const handleFollowUpSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleSubmit(e);
  };

  const handleCancelDeepResearch = () => {
    setShowDeepResearchConfirm(false);
  };

  const handleCancelDeepSeek = () => {
    setShowDeepSeekConfirm(false);
  };
  
  // Add a new function to handle example query selection
  const handleExampleQuerySelect = (query: string, queryMode?: string) => {
    setQuery(query);
    // If a mode is specified with the query, update the search mode
    if (queryMode) {
      setMode(queryMode);
    }
  };
  
  return (
    <div className="flex flex-col h-screen overflow-hidden">
      {/* News Ticker Banner */}
      <NewsTickerBanner />
      
      {/* Main Content */}
      <div className="flex flex-col md:flex-row flex-1 overflow-hidden">
        {/* Sidebar */}
        <Sidebar />
        
        {/* Main Content Area */}
        <div className="flex-1 overflow-y-auto bg-slate-50 dark:bg-slate-900 p-2 md:p-4">
          {/* Mobile Header - Only visible on small screens - REMOVED */}
          
          {/* Hero Section with Enhanced Search - Reduced spacing */}
          <div className={`flex flex-col items-center justify-center ${!loading && results.length === 0 ? 'min-h-[15vh] mb-3' : 'min-h-[5vh] mb-1'} px-4`}>
            {/* Logo - Only show when not loading and no results */}
            {!loading && results.length === 0 && (
              <div className="mb-3">
                <img 
                  src="/nexevon-black-logo.png" 
                  alt="Nexevon - AI Financial Research Intelligence" 
                  className="h-16 md:h-20 w-auto mx-auto"
                />
              </div>
            )}
            
            {/* Tagline - Only show when not loading and no results */}
            {!loading && results.length === 0 && (
              <p className="text-sm md:text-base text-center text-slate-600 dark:text-slate-400 mb-4 max-w-2xl">
                Ask anything about stocks, markets, and investment trends—our AI delivers deep, data-driven answers in real time.
              </p>
            )}
            
            {/* Enhanced Search Bar - Only show when not loading and no results */}
            {!loading && results.length === 0 && (
              <div className="w-full flex justify-center">
                <SearchBar 
                  query={query}
                  setQuery={setQuery}
                  mode={mode}
                  setMode={setMode}
                  useStreaming={useStreaming}
                  setUseStreaming={setUseStreaming}
                  onSubmit={handleSubmit}
                  loading={loading}
                />
              </div>
            )}
            
            {/* Example Queries - Only show when not loading and no results */}
            {!loading && results.length === 0 && (
              <ExampleQueries setQuery={handleExampleQuerySelect} />
            )}
          </div>
          
          {/* Market Data Section */}
          {!loading && results.length === 0 && (
            <div className="space-y-4">
              {/* Market Sentiment Panel */}
              <MarketSentimentPanel />
              
              {/* Market Snapshot */}
              <MarketSnapshot />
            </div>
          )}
          
          {/* Deep Research Confirmation Modal */}
          {showDeepResearchConfirm && (
            <div className="fixed inset-0 z-50 flex items-center justify-center pointer-events-none">
              <div className="pointer-events-auto bg-white dark:bg-slate-800 rounded-xl shadow-xl max-w-md w-full p-6 animate-fadeIn border border-slate-200 dark:border-slate-700">
                <h3 className="text-xl font-bold mb-4">Use Deep Research Mode?</h3>
                <p className="mb-6 text-slate-600 dark:text-slate-400">
                  Deep Research mode performs comprehensive analysis across multiple data sources. This may take longer but provides more detailed insights.
                </p>
                <div className="flex justify-end space-x-3">
                  <button
                    onClick={handleCancelDeepResearch}
                    className="px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleSubmit}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg"
                  >
                    Proceed
                  </button>
                </div>
              </div>
            </div>
          )}
          
          {/* DeepSeek Confirmation Modal */}
          {showDeepSeekConfirm && (
            <div className="fixed inset-0 z-50 flex items-center justify-center pointer-events-none">
              <div className="pointer-events-auto bg-white dark:bg-slate-800 rounded-xl shadow-xl max-w-md w-full p-6 animate-fadeIn border border-slate-200 dark:border-slate-700">
                <h3 className="text-xl font-bold mb-4">Use Comprehensive Research Mode?</h3>
                <p className="mb-6 text-slate-600 dark:text-slate-400">
                  Comprehensive mode uses our most advanced AI model to provide professional-grade financial analysis. This may take longer but delivers the most thorough insights.
                </p>
                <div className="flex justify-end space-x-3">
                  <button
                    onClick={handleCancelDeepSeek}
                    className="px-4 py-2 border border-slate-300 dark:border-slate-600 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleSubmit}
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg"
                  >
                    Proceed
                  </button>
                </div>
              </div>
            </div>
          )}
          
          {/* Search Results */}
          <SearchResults 
            results={results}
            loading={loading}
            query={query}
            statusMessages={statusMessages}
            isFollowUpQuestion={isFollowUpQuestion}
            sessionId={sessionId}
            handleFollowUpSubmit={handleFollowUpSubmit}
            setQuery={setQuery}
          />
          
          {/* Error Display */}
          {error && (
            <div className="max-w-4xl mx-auto mt-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl text-red-600 dark:text-red-400">
              <p className="flex items-center">
                <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 8V12M12 16H12.01M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                {error}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
