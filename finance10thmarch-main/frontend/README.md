# Financial Search Engine Frontend

This is the frontend component of the AI Financial Search Engine, built with Next.js and React. It provides a modern, responsive interface for interacting with the financial search engine.

## Features

- **Modern UI**: Clean, responsive design built with Next.js and Tailwind CSS
- **Real-time Streaming**: Display of streaming responses as they're generated
- **Markdown Rendering**: Beautiful rendering of structured financial reports
- **Multiple Search Modes**: Support for different search modes (Sonar, Deep Research, DeepSeek)
- **Progress Updates**: Real-time status updates during API calls
- **Conversation History**: Tracking of previous queries and responses

## Architecture

The frontend follows a modern React architecture:

- **Next.js Framework**: For server-side rendering and routing
- **React Hooks**: For state management and side effects
- **Tailwind CSS**: For utility-first styling
- **Fetch API**: For communication with the backend
- **ReactMarkdown**: For rendering markdown content from the backend

## Components

### Main Page (`app/page.tsx`)

The main page component handles:
- User input and form submission
- Search mode selection
- Streaming response handling
- Rendering of search results
- Progress updates display

### Markdown Renderer

The application uses ReactMarkdown with custom styling to render the structured financial reports from DeepSeek R1, including:
- Headings and subheadings
- Lists and bullet points
- Tables for financial data
- Links to sources
- Code blocks for technical data

## Search Modes

### Sonar Mode
- Quick search for market insights and news
- Faster response times
- Good for simple queries

### Deep Research Mode
- In-depth analysis using Perplexity's deep research capabilities
- More comprehensive but slower
- Good for complex queries requiring detailed analysis

### DeepSeek Mode
- Professional-grade financial research reports
- Comprehensive analysis with executive summaries and recommendations
- Structured format with sections and subsections
- Includes reasoning process for transparency

## Getting Started

### Prerequisites
- Node.js 14+
- Backend server running (see backend README)

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

### Configuration

The frontend is configured through environment variables in a `.env.local` file:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Development

### Project Structure

```
frontend/
├── public/          # Static assets
├── src/
│   ├── app/         # Next.js app directory
│   │   ├── page.tsx # Main page component
│   │   └── layout.tsx # Layout component
│   ├── components/  # Reusable components
│   └── styles/      # Global styles
├── next.config.js   # Next.js configuration
└── tailwind.config.js # Tailwind CSS configuration
```

### Adding New Features

1. **New Components**:
   - Create component files in `src/components/`
   - Import and use them in page components

2. **New Pages**:
   - Add new page components in `src/app/`
   - Next.js will automatically create routes based on the file structure

3. **Styling**:
   - Use Tailwind CSS utility classes for styling
   - Add custom styles in `src/styles/` if needed

## Future Enhancements

- **Interactive Charts**: Visualization of financial data
- **User Authentication**: Personalized experience and saved searches
- **Dark Mode**: Toggle between light and dark themes
- **Export Options**: Download reports in PDF or other formats
- **Mobile App**: Progressive Web App (PWA) support
- **Voice Input**: Speech-to-text for query input
- **Streaming Reasoning Display**: Real-time display of DeepSeek's reasoning process

## Troubleshooting

### Common Issues

- **API Connection Errors**: Ensure the backend server is running
- **Rendering Issues**: Check for markdown formatting problems
- **Slow Performance**: Optimize component rendering and reduce unnecessary re-renders
- **Streaming Issues**: Verify browser support for Server-Sent Events

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://reactjs.org/docs/getting-started.html)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [ReactMarkdown Documentation](https://github.com/remarkjs/react-markdown)

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
