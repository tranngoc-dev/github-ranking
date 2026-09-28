import React from 'react';
import { promises as fs } from 'fs';
import path from 'path';
import ProjectList from '@/components/ProjectList';
import { Project } from '@/components/ProjectCard';

async function getProjects() {
  const filePath = path.join(process.cwd(), 'src/data/projects.json');
  const fileContent = await fs.readFile(filePath, 'utf8');
  return JSON.parse(fileContent) as Project[];
}

async function getCategories() {
  const filePath = path.join(process.cwd(), 'src/data/categories.json');
  const fileContent = await fs.readFile(filePath, 'utf8');
  return JSON.parse(fileContent) as { id: string, name: string }[];
}

export default async function Home() {
  let projects: Project[] = [];
  let categories: { id: string, name: string }[] = [];
  
  try {
    projects = await getProjects();
    categories = await getCategories();
  } catch (error) {
    console.error('Failed to load data:', error);
  }

  const totalStars = projects.reduce((acc, curr) => acc + curr.stars, 0);

  return (
    <div className="container mx-auto px-4 py-8 md:py-12">
      <div className="mb-12 flex flex-col items-center text-center space-y-4">
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-slate-900">
          Khám phá <span className="text-primary bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">GitHub Ranking</span>
        </h1>
        <p className="max-w-2xl text-lg text-slate-600">
          Top 5.500+ dự án mã nguồn mở nhiều sao nhất thế giới (&gt;= 10.000 ⭐) cập nhật trực tiếp từ GitHub.
        </p>
        
        <div className="flex flex-wrap justify-center gap-4 mt-6">
          <div className="flex flex-col items-center p-4 bg-slate-50 rounded-2xl min-w-[120px]">
            <span className="text-3xl font-bold text-slate-900">{projects.length}+</span>
            <span className="text-sm font-medium text-slate-500">Dự án</span>
          </div>
          <div className="flex flex-col items-center p-4 bg-slate-50 rounded-2xl min-w-[120px]">
            <span className="text-3xl font-bold text-slate-900">{(totalStars / 1000).toFixed(0)}k+</span>
            <span className="text-sm font-medium text-slate-500">Tổng Stars</span>
          </div>
          <div className="flex flex-col items-center p-4 bg-slate-50 rounded-2xl min-w-[120px]">
            <span className="text-3xl font-bold text-slate-900">{categories.length}</span>
            <span className="text-sm font-medium text-slate-500">Chủ đề</span>
          </div>
        </div>
      </div>

      <ProjectList initialProjects={projects} categories={categories} />
    </div>
  );
}
