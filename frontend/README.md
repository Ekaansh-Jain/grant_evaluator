# Grant Evaluator Frontend

React + TypeScript + Vite frontend for the AI Grant Evaluator application.

## Features

- **Modern UI**: Beautiful dark-themed interface with gradient accents
- **File Upload**: Drag & drop or browse for PDF/DOCX grant proposals
- **Real-time Evaluation**: Upload files and see comprehensive AI-powered analysis
- **Interactive Dashboards**: Visualize scores with radar charts and bar charts
- **Detailed Reporting**: View scores, critiques, budget analysis, and recommendations
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Prerequisites

- Node.js 18+ and npm
- Backend API running on port 8000 (see `../backend/README.md`)

## Setup

### 1. Install Dependencies

```bash
cd project
npm install
```

### 2. Configure Environment

Create a `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` if your backend runs on a different port:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

### 3. Run Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Lint code
- `npm run typecheck` - Type check TypeScript

## Project Structure

```
project/
├── src/
│   ├── components/       # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Navbar.tsx
│   │   ├── Tabs.tsx
│   │   └── charts/       # Chart components
│   ├── pages/            # Page components
│   │   ├── Home.tsx      # File upload page
│   │   ├── Results.tsx   # Evaluation results
│   │   └── Settings.tsx  # App settings
│   ├── services/         # API services
│   │   └── evaluationService.ts
│   ├── types/            # TypeScript type definitions
│   │   └── evaluation.ts
│   ├── App.tsx           # Main app component
│   └── main.tsx          # Entry point
├── package.json
└── vite.config.ts
```

## API Integration

The frontend communicates with the FastAPI backend via REST endpoints:

- `POST /api/evaluations` - Upload and evaluate grant
- `GET /api/evaluations` - Get all evaluations
- `GET /api/evaluations/:id` - Get specific evaluation
- `GET /api/settings` - Get settings
- `PUT /api/settings` - Update settings

## Technology Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Tailwind CSS** - Utility-first styling
- **Chart.js** - Data visualization
- **Lucide React** - Icon library

## Building for Production

```bash
npm run build
```

The optimized production build will be in the `dist/` directory.

### Deploy to Vercel/Netlify

1. Push your code to GitHub
2. Connect your repository to Vercel or Netlify
3. Set the environment variable `VITE_API_BASE_URL` to your production API URL
4. Deploy!

## Troubleshooting

### Backend Connection Issues

If you see "Failed to fetch" errors:

1. Make sure the backend is running on `http://localhost:8000`
2. Check that CORS is enabled in the backend
3. Verify the `VITE_API_BASE_URL` in `.env` is correct

### Build Errors

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Type check
npm run typecheck
```

## Changes from Original

### Removed Supabase

This version uses a custom FastAPI backend with MongoDB Atlas instead of Supabase:

- ✅ No Supabase dependency
- ✅ Direct file upload to backend
- ✅ RESTful API integration
- ✅ MongoDB Atlas for data persistence

### Updated Files

- `src/services/evaluationService.ts` - Now uses fetch API instead of Supabase client
- `src/pages/Home.tsx` - Direct file upload to backend
- `package.json` - Removed `@supabase/supabase-js` dependency
- Deleted `src/lib/supabase.ts`

## License

MIT
