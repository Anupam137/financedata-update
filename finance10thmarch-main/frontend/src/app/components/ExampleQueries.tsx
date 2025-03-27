'use client';

interface ExampleQueriesProps {
  setQuery: (query: string, mode?: string) => void;
}

const exampleQueries = [
  // Basic queries (Sonar mode)
  {
    text: "What's the sentiment around NVDA?",
    category: "Sentiment",
    mode: "sonar"
  },
  {
    text: "Bitcoin price prediction",
    category: "Crypto",
    mode: "sonar"
  },
  
  // Deep Research queries
  {
    text: "Compare AAPL and MSFT fundamentals",
    category: "Comparison",
    mode: "deep_research"
  },
  {
    text: "Analyze Tesla's valuation based on 2025 projections",
    category: "Analysis",
    mode: "deep_research"
  },
  {
    text: "How will rising interest rates affect tech stocks?",
    category: "Macro",
    mode: "deep_research"
  },
  
  // Comprehensive Research queries
  {
    text: "Build a DCF model for Amazon",
    category: "Valuation",
    mode: "deepseek"
  },
  {
    text: "Analyze semiconductor industry supply chain risks",
    category: "Industry",
    mode: "deepseek"
  },
  {
    text: "Evaluate ESG impact on energy sector returns",
    category: "Strategy",
    mode: "deepseek"
  }
];

export default function ExampleQueries({ setQuery }: ExampleQueriesProps) {
  return (
    <div className="max-w-4xl mx-auto mt-4">
      <h3 className="text-xs font-medium text-slate-500 dark:text-slate-400 mb-2 text-center">Every financial data point at your fingertips:</h3>
      
      <div className="flex flex-wrap justify-center gap-1.5">
        {exampleQueries.map((example, index) => (
          <button
            key={index}
            onClick={() => setQuery(example.text, example.mode)}
            className={`px-2.5 py-1 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-full text-xs hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors group ${
              example.mode === 'deep_research' ? 'border-purple-200 dark:border-purple-800' : 
              example.mode === 'deepseek' ? 'border-teal-200 dark:border-teal-800' : 
              'border-slate-200 dark:border-slate-700'
            }`}
          >
            <span className={`mr-1 group-hover:text-blue-500 transition-colors ${
              example.mode === 'deep_research' ? 'text-purple-400 dark:text-purple-500' : 
              example.mode === 'deepseek' ? 'text-teal-400 dark:text-teal-500' : 
              'text-slate-400 dark:text-slate-500'
            }`}>#</span>
            <span className={`text-slate-700 dark:text-slate-300 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors ${
              example.mode === 'deep_research' ? 'text-purple-700 dark:text-purple-300' : 
              example.mode === 'deepseek' ? 'text-teal-700 dark:text-teal-300' : 
              ''
            }`}>{example.text}</span>
          </button>
        ))}
      </div>
      
      <div className="mt-4 text-center">
        <p className="text-xs text-slate-500 dark:text-slate-400">
          <span className="inline-block mx-1 px-1.5 py-0.5 bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 rounded-full text-xs">Pro Search</span>
          <span className="inline-block mx-1 px-1.5 py-0.5 bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300 rounded-full text-xs">Deep Research</span>
          <span className="inline-block mx-1 px-1.5 py-0.5 bg-teal-100 dark:bg-teal-900 text-teal-700 dark:text-teal-300 rounded-full text-xs">Comprehensive</span>
        </p>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-2">
          <span className="font-bold">Pro Search</span>: Quick answers • <span className="font-bold">Deep Research</span>: Detailed analysis • <span className="font-bold">Comprehensive</span>: Professional insights
        </p>
      </div>
    </div>
  );
} 