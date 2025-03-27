'use client';

import { useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import SourceCards from './SourceCards';

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

interface SearchResultsProps {
  results: {query: string, result: SearchResult}[];
  loading: boolean;
  query: string;
  statusMessages: string[];
  isFollowUpQuestion: boolean;
  sessionId: string | null;
  handleFollowUpSubmit: (e: React.FormEvent) => void;
  setQuery: (query: string) => void;
}

export default function SearchResults({
  results,
  loading,
  query,
  statusMessages,
  isFollowUpQuestion,
  sessionId,
  handleFollowUpSubmit,
  setQuery
}: SearchResultsProps) {
  const resultContainerRef = useRef<HTMLDivElement>(null);
  const latestResultRef = useRef<HTMLDivElement>(null);
  
  // Show loading state alone if no results yet
  if (results.length === 0 && loading) {
    return (
      <div className="bg-white dark:bg-slate-800 rounded-xl shadow-md p-5 mb-4 max-w-5xl mx-auto px-4 md:px-4">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-base font-medium">
            <span className="inline-flex items-center">
              <span className="animate-pulse mr-2">🔍</span>
              <span className="text-slate-800 dark:text-slate-200">
                {query}
              </span>
            </span>
          </h3>
          {isFollowUpQuestion && (
            <span className="bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs font-medium px-2 py-0.5 rounded">
              Follow-up Question
            </span>
          )}
        </div>
        
        {isFollowUpQuestion && sessionId && (
          <div className="mt-2 mb-4 text-sm text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/30 p-2 rounded">
            <p className="flex items-center">
              <svg className="w-4 h-4 mr-2" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M12 8V12L15 15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              Using conversation context from previous exchanges
            </p>
          </div>
        )}
        
        {statusMessages.length > 0 && (
          <div className="mt-4 border-t border-slate-200 dark:border-slate-700 pt-3">
            <h3 className="text-sm font-medium mb-2 flex items-center">
              <span className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></span>
              <span className="text-slate-800 dark:text-slate-200">
                AI agents scanning real-time data:
              </span>
            </h3>
            <ul className="space-y-2">
              {statusMessages.map((message, index) => (
                <li 
                  key={index} 
                  className="flex items-center text-sm opacity-0 animate-slide-in"
                  style={{ animationDelay: `${index * 150}ms` }}
                >
                  <span className="flex items-center justify-center w-5 h-5 rounded-full bg-blue-100 dark:bg-blue-900 mr-2">
                    <span className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-ping"></span>
                  </span>
                  <span className="text-slate-700 dark:text-slate-300">
                    {message}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  }
  
  // Show loading indicator if more results are being loaded
  const LoadingIndicator = () => (
    <div className="flex justify-center items-center py-4">
      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
      <p className="ml-3 text-base">Loading more results...</p>
    </div>
  );
  
  // Display all results in sequence
  if (results.length > 0) {
    return (
      <>
        <div ref={resultContainerRef} className="max-w-5xl mx-auto pb-16 px-4 md:px-4">
          {results.map((item, index) => (
            <div 
              key={index} 
              ref={index === results.length - 1 && !loading ? latestResultRef : null}
              className="bg-white dark:bg-slate-800 rounded-xl shadow-md p-5 mb-5 animate-fade-in"
              style={{ animationDelay: `${index * 150}ms` }}
            >
              <div className="flex justify-between items-center mb-4">
                <div className="flex items-center">
                  <div className="w-5 h-5 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center text-blue-600 dark:text-blue-300 mr-2">
                    <svg className="w-3 h-3" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" fill="currentColor" fillOpacity="0.2"/>
                      <path d="M12 8V12L15 15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  </div>
                  <h3 className="text-sm font-medium">{item.query}</h3>
                </div>
                {index > 0 && (
                  <span className="bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs font-medium px-2 py-0.5 rounded">
                    Follow-up Question
                  </span>
                )}
              </div>
              
              {/* Sources Cards - Display at the top */}
              {item.result.sources && item.result.sources.length > 0 && (
                <div className="mb-4">
                  <SourceCards sources={item.result.sources} />
                </div>
              )}
              
              <div className="prose prose-sm prose-blue dark:prose-invert max-w-none">
                <ReactMarkdown 
                  remarkPlugins={[remarkGfm]}
                  components={{
                    h1: ({...props}) => <h1 className="text-xl font-bold mt-6 mb-4 text-slate-800 dark:text-slate-200" {...props} />,
                    h2: ({...props}) => <h2 className="text-lg font-bold mt-5 mb-3 text-slate-800 dark:text-slate-200" {...props} />,
                    h3: ({...props}) => <h3 className="text-base font-bold mt-4 mb-3 text-slate-800 dark:text-slate-200" {...props} />,
                    h4: ({...props}) => <h4 className="text-base font-bold mt-3 mb-2 text-slate-800 dark:text-slate-200" {...props} />,
                    p: ({...props}) => <p className="my-4 text-base text-slate-700 dark:text-slate-300" {...props} />,
                    ul: ({...props}) => <ul className="list-disc pl-5 my-4 space-y-2" {...props} />,
                    ol: ({...props}) => <ol className="list-decimal pl-5 my-4 space-y-2" {...props} />,
                    li: ({...props}) => <li className="mb-2.5 text-base" {...props} />,
                    a: ({...props}) => <a className="text-blue-600 dark:text-blue-400 hover:underline" {...props} />,
                    blockquote: ({...props}) => <blockquote className="border-l-4 border-slate-200 dark:border-slate-700 pl-4 my-4 text-slate-600 dark:text-slate-400 text-base py-0.5" {...props} />,
                    strong: ({...props}) => <strong className="font-bold text-slate-900 dark:text-slate-100" {...props} />,
                    code: ({...props}) => <code className="bg-slate-100 dark:bg-slate-700 rounded px-1 py-0.5 text-sm font-mono" {...props} />,
                    table: ({...props}) => <div className="overflow-x-auto my-5"><table className="min-w-full divide-y divide-slate-200 dark:divide-slate-700 text-base" {...props} /></div>,
                    thead: ({...props}) => <thead className="bg-slate-50 dark:bg-slate-800" {...props} />,
                    th: ({...props}) => <th className="px-3 py-2.5 text-left text-sm font-semibold text-slate-900 dark:text-slate-100" {...props} />,
                    td: ({...props}) => <td className="whitespace-nowrap px-3 py-2.5 text-sm text-slate-700 dark:text-slate-300" {...props} />,
                  }}
                >
                  {item.result.answer}
                </ReactMarkdown>
              </div>
            </div>
          ))}
          
          {/* Show loading indicator if more results are being loaded */}
          {loading && <LoadingIndicator />}
        </div>

        {/* Sticky Follow-up Search Bar */}
        {!loading && results.length > 0 && (
          <div className="fixed bottom-0 left-0 right-0 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-700 shadow-lg p-1.5 z-50">
            <div className="max-w-5xl mx-auto px-4 md:px-4">
              <form onSubmit={handleFollowUpSubmit} className="space-y-1">
                <div className="flex flex-col md:flex-row gap-2">
                  <div className="flex-1 relative">
                    <input
                      type="text"
                      value={query}
                      onChange={(e) => setQuery(e.target.value)}
                      placeholder="Ask a follow-up question..."
                      className="w-full px-4 py-2 pr-28 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 text-slate-900 dark:text-slate-100 text-sm"
                    />
                    <button
                      type="submit"
                      disabled={loading}
                      className="absolute right-2 top-1/2 transform -translate-y-1/2 px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-full transition-colors disabled:bg-blue-400 text-xs"
                    >
                      Ask Follow-up
                    </button>
                  </div>
                </div>
                {sessionId && (
                  <div className="text-xs text-slate-500 dark:text-slate-400 mt-0.5 flex items-center">
                    <svg className="w-3 h-3 mr-1" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      <path d="M12 8V12L15 15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                    Using conversation context from session: {sessionId.substring(0, 8)}...
                  </div>
                )}
              </form>
            </div>
          </div>
        )}
      </>
    );
  }
  
  // Default empty state
  return null;
} 