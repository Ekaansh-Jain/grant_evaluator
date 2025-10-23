import { useState, useRef, DragEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, FileText, X } from 'lucide-react';
import { Button } from '../components/Button';
import { LoadingAnimation } from '../components/LoadingAnimation';
import { evaluationService } from '../services/evaluationService';

export function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isEvaluating, setIsEvaluating] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();

  const handleDragOver = (e: DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && isValidFile(droppedFile)) {
      setFile(droppedFile);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile && isValidFile(selectedFile)) {
      setFile(selectedFile);
    }
  };

  const isValidFile = (file: File) => {
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    return validTypes.includes(file.type);
  };

  const handleEvaluate = async () => {
    if (!file) return;

    setIsEvaluating(true);

    try {
      // Upload file directly to backend for evaluation
      const saved = await evaluationService.saveEvaluation(file);
      navigate(`/results/${saved.id}`);
    } catch (error) {
      console.error('Evaluation failed:', error);
      alert('Evaluation failed. Please try again.');
      setIsEvaluating(false);
    }
  };

  const removeFile = () => {
    setFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center p-4">
      {isEvaluating && <LoadingAnimation />}

      <div className="max-w-4xl w-full space-y-8">
        <div className="text-center space-y-4 animate-fade-in">
          <h1 className="text-5xl md:text-6xl font-bold gradient-text">
            AI Grant Evaluator
          </h1>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto">
            Upload your grant proposal and receive comprehensive, AI-powered evaluation with detailed scoring, critiques, and actionable recommendations.
          </p>
        </div>

        <div className="card-premium p-8 md:p-12 animate-slide-up">
          <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            className={`border-2 border-dashed rounded-2xl p-12 text-center transition-all duration-300 ${
              isDragging
                ? 'border-accent-magenta bg-accent-magenta/10 scale-105'
                : 'border-charcoal-700 hover:border-accent-purple hover:bg-charcoal-900/50'
            }`}
          >
            {!file ? (
              <>
                <div className="flex justify-center mb-6">
                  <div className="w-20 h-20 rounded-2xl bg-gradient-primary flex items-center justify-center shadow-glow-purple">
                    <Upload className="w-10 h-10 text-white" />
                  </div>
                </div>
                <h3 className="text-2xl font-semibold text-gray-200 mb-2">
                  Drag & Drop Your Grant
                </h3>
                <p className="text-gray-400 mb-6">
                  or click to browse files (PDF, DOCX)
                </p>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".pdf,.docx"
                  onChange={handleFileSelect}
                  className="hidden"
                  id="file-upload"
                />
                <label htmlFor="file-upload" className="cursor-pointer">
                  <span className="inline-block border-2 border-accent-purple text-accent-purple hover:bg-accent-purple hover:text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300">
                    Browse Files
                  </span>
                </label>
              </>
            ) : (
              <div className="space-y-6">
                <div className="flex items-center justify-between p-4 bg-charcoal-900 rounded-xl">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 rounded-lg bg-gradient-primary flex items-center justify-center">
                      <FileText className="w-6 h-6 text-white" />
                    </div>
                    <div className="text-left">
                      <p className="font-medium text-gray-200">{file.name}</p>
                      <p className="text-sm text-gray-500">
                        {(file.size / 1024 / 1024).toFixed(2)} MB
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={removeFile}
                    className="p-2 hover:bg-charcoal-800 rounded-lg transition-colors"
                  >
                    <X className="w-5 h-5 text-gray-400 hover:text-error" />
                  </button>
                </div>
                <Button onClick={handleEvaluate} className="w-full" size="lg">
                  Evaluate Grant
                </Button>
              </div>
            )}
          </div>

          <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center p-6 bg-charcoal-900/50 rounded-xl">
              <div className="text-3xl font-bold gradient-text mb-2">8.5/10</div>
              <p className="text-sm text-gray-400">Average Score</p>
            </div>
            <div className="text-center p-6 bg-charcoal-900/50 rounded-xl">
              <div className="text-3xl font-bold gradient-text mb-2">7</div>
              <p className="text-sm text-gray-400">Critique Domains</p>
            </div>
            <div className="text-center p-6 bg-charcoal-900/50 rounded-xl">
              <div className="text-3xl font-bold gradient-text mb-2">10</div>
              <p className="text-sm text-gray-400">Section Scores</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
