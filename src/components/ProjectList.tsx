'use client';

import React, { useState, useMemo } from 'react';
import Fuse from 'fuse.js';
import { Search, SlidersHorizontal, ArrowDownAZ } from 'lucide-react';
import { ProjectCard, Project } from './ProjectCard';
import { ProjectModal } from './ProjectModal';

interface ProjectListProps {
  initialProjects: Project[];
  categories: { id: string, name: string }[];
}

export default function ProjectList({ initialProjects, categories }: ProjectListProps) {
  const [query, setQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedYear, setSelectedYear] = useState<string>('all');
  const [sortBy, setSortBy] = useState<'stars' | 'name'>('stars');
  
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);

  const fuse = useMemo(() => new Fuse(initialProjects, {
    keys: ['name', 'summaryVi', 'description_zh'],
    threshold: 0.4,
  }), [initialProjects]);

  const filteredProjects = useMemo(() => {
    let result = initialProjects;

    // Search
    if (query) {
      result = fuse.search(query).map(r => r.item);
    }

    // Filter
    if (selectedCategory !== 'all') {
      result = result.filter(p => p.categoryVi === selectedCategory);
    }
    if (selectedYear !== 'all') {
      result = result.filter(p => p.year.toString() === selectedYear);
    }

    // Sort
    result = [...result].sort((a, b) => {
      if (sortBy === 'stars') {
        return b.stars - a.stars;
      } else {
        return a.name.localeCompare(b.name);
      }
    });

    return result;
  }, [initialProjects, query, selectedCategory, selectedYear, sortBy, fuse]);

  return (
    <div className="w-full">
      {/* Search & Filter Bar */}
      <div className="sticky top-14 z-40 mb-8 rounded-xl border bg-background/95 p-4 shadow-sm backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="flex flex-col gap-4 md:flex-row md:items-center">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <input
              type="text"
              placeholder="Tìm kiếm dự án (VD: công cụ AI, automation...)"
              className="h-10 w-full rounded-md border border-input bg-background pl-9 pr-4 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </div>
          
          <div className="flex flex-wrap items-center gap-2">
            <div className="flex items-center space-x-2 rounded-md border border-input bg-background px-3 h-10">
              <SlidersHorizontal className="h-4 w-4 text-muted-foreground" />
              <select 
                className="bg-transparent text-sm outline-none w-[130px] cursor-pointer"
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
              >
                <option value="all">Tất cả danh mục</option>
                {categories.map(c => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
            </div>

            <div className="flex items-center space-x-2 rounded-md border border-input bg-background px-3 h-10">
              <select 
                className="bg-transparent text-sm outline-none cursor-pointer"
                value={selectedYear}
                onChange={(e) => setSelectedYear(e.target.value)}
              >
                <option value="all">Mọi năm</option>
                <option value="2025">2025</option>
                <option value="2024">2024</option>
              </select>
            </div>

            <div className="flex items-center space-x-2 rounded-md border border-input bg-background px-3 h-10">
              <ArrowDownAZ className="h-4 w-4 text-muted-foreground" />
              <select 
                className="bg-transparent text-sm outline-none cursor-pointer"
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as 'stars' | 'name')}
              >
                <option value="stars">Nhiều Stars nhất</option>
                <option value="name">Tên A-Z</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Results stats */}
      <div className="mb-6 text-sm text-muted-foreground">
        Hiển thị <strong>{filteredProjects.length}</strong> dự án {query && `phù hợp với "${query}"`}
      </div>

      {/* Grid */}
      {filteredProjects.length > 0 ? (
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {filteredProjects.map((project) => (
            <ProjectCard 
              key={project.id} 
              project={project} 
              onClick={() => setSelectedProject(project)} 
            />
          ))}
        </div>
      ) : (
        <div className="flex min-h-[400px] flex-col items-center justify-center rounded-xl border border-dashed text-center">
          <div className="rounded-full bg-slate-100 p-3 mb-4">
            <Search className="h-6 w-6 text-slate-400" />
          </div>
          <h3 className="text-lg font-semibold text-slate-900">Không tìm thấy dự án nào</h3>
          <p className="text-slate-500 max-w-sm mt-1">
            Hãy thử thay đổi từ khóa hoặc bộ lọc để tìm được dự án bạn cần nhé.
          </p>
          <button 
            onClick={() => {
              setQuery('');
              setSelectedCategory('all');
              setSelectedYear('all');
            }}
            className="mt-6 font-medium text-primary hover:underline"
          >
            Xóa tất cả bộ lọc
          </button>
        </div>
      )}

      {/* Modal */}
      <ProjectModal 
        project={selectedProject} 
        onClose={() => setSelectedProject(null)} 
        categories={categories}
      />
    </div>
  );
}
