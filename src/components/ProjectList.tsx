'use client';

import React, { useState, useMemo, useEffect } from 'react';
import Fuse from 'fuse.js';
import { Search, SlidersHorizontal, ArrowDownAZ, ChevronLeft, ChevronRight, Star } from 'lucide-react';
import { ProjectCard, Project } from './ProjectCard';
import { ProjectModal } from './ProjectModal';

interface ProjectListProps {
  initialProjects: Project[];
  categories: { id: string, name: string }[];
}

const PAGE_SIZE = 24;

export default function ProjectList({ initialProjects, categories }: ProjectListProps) {
  const [query, setQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedYear, setSelectedYear] = useState<string>('all');
  const [minStars, setMinStars] = useState<number>(0);
  const [sortBy, setSortBy] = useState<'stars' | 'name'>('stars');
  
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);

  // Reset to page 1 on filter change
  useEffect(() => {
    setCurrentPage(1);
  }, [query, selectedCategory, selectedYear, minStars, sortBy]);

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
    if (selectedCategory === 'top-1000') {
      result = result.filter(p => p.isTop1000 === true || p.categoryVi === 'top-1000');
    } else if (selectedCategory !== 'all') {
      result = result.filter(p => p.categoryVi === selectedCategory);
    }
    if (selectedYear !== 'all') {
      result = result.filter(p => p.year.toString() === selectedYear);
    }
    if (minStars > 0) {
      result = result.filter(p => p.stars >= minStars);
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
  }, [initialProjects, query, selectedCategory, selectedYear, minStars, sortBy, fuse]);

  const totalPages = Math.ceil(filteredProjects.length / PAGE_SIZE);
  const paginatedProjects = filteredProjects.slice((currentPage - 1) * PAGE_SIZE, currentPage * PAGE_SIZE);

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
                className="bg-transparent text-sm outline-none w-auto min-w-[180px] max-w-[260px] cursor-pointer"
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
                <option value="2026">2026</option>
                <option value="2025">2025</option>
                <option value="2024">2024</option>
                <option value="2023">2023</option>
                <option value="2022">2022</option>
                <option value="2021">2021</option>
                <option value="2020">2020</option>
                <option value="2019">2019</option>
                <option value="2018">2018</option>
              </select>
            </div>

            <div className="flex items-center space-x-2 rounded-md border border-input bg-background px-3 h-10">
              <Star className="h-4 w-4 text-amber-500 fill-amber-500" />
              <select 
                className="bg-transparent text-sm outline-none cursor-pointer"
                value={minStars}
                onChange={(e) => {
                  setMinStars(Number(e.target.value));
                  setCurrentPage(1);
                }}
              >
                <option value="0">Tối thiểu: 0 ⭐</option>
                <option value="500">&gt; 500 ⭐</option>
                <option value="1000">&gt; 1.000 ⭐</option>
                <option value="5000">&gt; 5.000 ⭐</option>
                <option value="10000">&gt; 10.000 ⭐</option>
                <option value="20000">&gt; 20.000 ⭐</option>
                <option value="50000">&gt; 50.000 ⭐</option>
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
        <>
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {paginatedProjects.map((project) => (
              <ProjectCard 
                key={project.id} 
                project={project} 
                onClick={() => setSelectedProject(project)} 
              />
            ))}
          </div>

          {/* Pagination Controls */}
          {totalPages > 1 && (
            <div className="mt-8 flex items-center justify-center gap-2">
              <button
                onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                disabled={currentPage === 1}
                className="inline-flex h-9 w-9 items-center justify-center rounded-md border border-input bg-background text-sm font-medium shadow-sm transition-colors hover:bg-accent hover:text-accent-foreground disabled:pointer-events-none disabled:opacity-50"
              >
                <ChevronLeft className="h-4 w-4" />
              </button>
              
              <div className="flex items-center gap-1">
                {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                  let pageNum = currentPage;
                  if (totalPages <= 5) {
                    pageNum = i + 1;
                  } else if (currentPage <= 3) {
                    pageNum = i + 1;
                  } else if (currentPage >= totalPages - 2) {
                    pageNum = totalPages - 4 + i;
                  } else {
                    pageNum = currentPage - 2 + i;
                  }
                  
                  if (pageNum > 0 && pageNum <= totalPages) {
                    return (
                      <button
                        key={pageNum}
                        onClick={() => setCurrentPage(pageNum)}
                        className={`inline-flex h-9 w-9 items-center justify-center rounded-md border border-input text-sm font-medium shadow-sm transition-colors hover:bg-accent hover:text-accent-foreground ${
                          currentPage === pageNum 
                            ? "bg-primary text-primary-foreground hover:bg-primary/90" 
                            : "bg-background"
                        }`}
                      >
                        {pageNum}
                      </button>
                    );
                  }
                  return null;
                })}
              </div>

              <button
                onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                disabled={currentPage === totalPages}
                className="inline-flex h-9 w-9 items-center justify-center rounded-md border border-input bg-background text-sm font-medium shadow-sm transition-colors hover:bg-accent hover:text-accent-foreground disabled:pointer-events-none disabled:opacity-50"
              >
                <ChevronRight className="h-4 w-4" />
              </button>
              
              <span className="ml-4 text-sm text-muted-foreground">
                Trang {currentPage} / {totalPages}
              </span>
            </div>
          )}
        </>
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
              setMinStars(0);
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

