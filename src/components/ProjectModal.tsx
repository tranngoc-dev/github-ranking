import React, { useEffect } from 'react';
import { X, Star, Code, ExternalLink, Calendar, User, Tag } from 'lucide-react';
import { Project } from './ProjectCard';

interface ProjectModalProps {
  project: Project | null;
  onClose: () => void;
  categories: { id: string, name: string }[];
}

export function ProjectModal({ project, onClose, categories }: ProjectModalProps) {
  useEffect(() => {
    if (project) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
    return () => { document.body.style.overflow = 'unset'; }
  }, [project]);

  if (!project) return null;

  const categoryName = categories.find(c => c.id === project.categoryVi)?.name || 'Khác';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6">
      <div className="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity" onClick={onClose} />
      
      <div className="relative w-full max-w-2xl transform rounded-2xl bg-white dark:bg-slate-900 border dark:border-slate-800 p-6 text-left align-middle shadow-2xl transition-all h-auto max-h-[90vh] flex flex-col">
        <button 
          onClick={onClose}
          className="absolute right-4 top-4 rounded-full p-2 text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white transition-colors"
        >
          <X className="h-5 w-5" />
        </button>

        <div className="mb-6 pr-8">
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white flex items-center">
            {project.name}
          </h2>
          {project.isTop1000 && (
            <div className="mt-3">
              <span className="inline-flex items-center text-xs font-semibold text-amber-600 bg-amber-50 dark:bg-amber-950/40 px-2 py-1 rounded-md border border-amber-200 dark:border-amber-800">
                ⭐ Thuộc Top 1000 Dự Án Nhiều Sao Nhất Thế Giới
              </span>
            </div>
          )}
          <div className="mt-4 flex flex-wrap gap-3 text-sm text-slate-600">
            <span className="flex items-center"><User className="w-4 h-4 mr-1" /> {project.author}</span>
            <span className="flex items-center text-yellow-600"><Star className="w-4 h-4 mr-1" /> {(project.stars / 1000).toFixed(1)}k Stars</span>
            <span className="flex items-center"><Calendar className="w-4 h-4 mr-1" /> {project.year}</span>
            <span className="flex items-center"><Code className="w-4 h-4 mr-1" /> {project.language}</span>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto pr-2 pb-6">
          <div className="prose prose-slate max-w-none">
            <h3 className="text-lg font-semibold mb-2">Giới thiệu</h3>
            <p className="text-slate-700 leading-relaxed whitespace-pre-wrap">
              {project.summaryVi}
            </p>
          </div>
          
          <div className="mt-8 pt-6 border-t border-slate-100">
            <div className="flex items-center space-x-2 text-sm text-slate-500 mb-4">
              <Tag className="w-4 h-4" />
              <span>Phân loại: <strong className="text-slate-700 font-medium">{categoryName}</strong></span>
            </div>
            
            <a 
              href={project.repoUrl} 
              target="_blank" 
              rel="noreferrer"
              className="inline-flex w-full sm:w-auto items-center justify-center rounded-lg bg-slate-900 px-6 py-3 text-sm font-semibold text-white transition-colors hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-slate-900 focus:ring-offset-2"
            >
              <ExternalLink className="mr-2 h-4 w-4" />
              Xem trên GitHub
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
