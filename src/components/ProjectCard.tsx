import React from 'react';
import { Star, Code, ExternalLink, Copy, Check } from 'lucide-react';


export interface Project {
  id: string;
  name: string;
  repoUrl: string;
  author: string;
  categoryVi: string;
  summaryVi: string;
  stars: number;
  language: string;
  year: number;
}

export function ProjectCard({ project, onClick }: { project: Project, onClick: () => void }) {
  const [copied, setCopied] = React.useState(false);

  const copyUrl = (e: React.MouseEvent) => {
    e.stopPropagation();
    navigator.clipboard.writeText(project.repoUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const openLink = (e: React.MouseEvent) => {
    e.stopPropagation();
    window.open(project.repoUrl, '_blank');
  };

  return (
    <div 
      className="group relative flex flex-col items-start gap-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-card dark:bg-slate-900 p-5 text-card-foreground shadow-sm transition-all hover:shadow-md hover:border-primary/50 cursor-pointer h-full"
      onClick={onClick}
    >
      <div className="flex w-full items-start justify-between">
        <div className="space-y-1.5 flex-1 pr-4">
          <h3 className="font-semibold leading-none tracking-tight text-lg group-hover:text-primary dark:text-white transition-colors">
            {project.name}
          </h3>
          <p className="text-sm text-muted-foreground line-clamp-1">
            by {project.author} • {project.year}
          </p>
        </div>
        <div className="flex items-center space-x-1 rounded-md bg-secondary px-2.5 py-1 text-xs font-semibold text-secondary-foreground">
          <Star className="w-3 h-3 mr-1 text-yellow-500" />
          <span>{(project.stars / 1000).toFixed(1)}k</span>
        </div>
      </div>
      
      <p className="text-sm text-slate-600 line-clamp-3 flex-1 w-full">
        {project.summaryVi}
      </p>
      
      <div className="flex w-full items-center justify-between mt-auto pt-4 border-t border-slate-100">
        <div className="flex items-center text-xs font-medium text-slate-500">
          <Code className="w-3.5 h-3.5 mr-1.5" />
          {project.language}
        </div>
        
        <div className="flex space-x-2">
          <button 
            onClick={copyUrl}
            className="p-1.5 rounded-md text-slate-400 hover:text-slate-900 hover:bg-slate-100 transition-colors"
            title="Copy URL"
          >
            {copied ? <Check className="w-4 h-4 text-green-500" /> : <Copy className="w-4 h-4" />}
          </button>
          <button 
            onClick={openLink}
            className="p-1.5 rounded-md text-slate-400 hover:text-primary hover:bg-primary/10 transition-colors"
            title="Open in GitHub"
          >
            <ExternalLink className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
