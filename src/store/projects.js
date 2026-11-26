import { defineStore } from 'pinia'
import { useTasksStore } from './tasks.js'

export const useProjectsStore = defineStore('projects', {
  state: () => ({
    projects: [
      { id: 'general', title: 'Загальні' },
      { id: 'study', title: 'Навчання' },
      { id: 'personal', title: 'Особисті' },
    ],
    nextProjectId: 1,
  }),
  getters: {
    projectCount: state => state.projects.length,
    projectTitle: state => id => state.projects.find(project => project.id === id)?.title ?? 'Загальні',
    projectStats(state) {
      const stats = Object.fromEntries(state.projects.map(({ id }) => [
        id, { total: 0, completed: 0, incomplete: 0, percent: 0 },
      ]))
      for (const task of useTasksStore().tasks) {
        const project = stats[task.projectId] ?? stats.general
        project.total++
        if (task.status === 'done') project.completed++
        else project.incomplete++
      }
      for (const project of Object.values(stats)) {
        project.percent = project.total ? Math.round(project.completed / project.total * 100) : 0
      }
      return stats
    },
  },
  actions: {
    addProject(rawTitle) {
      const title = String(rawTitle ?? '').trim()
      if (title.length < 3 || title.length > 40) return null
      const normalized = title.toLocaleLowerCase('uk-UA')
      if (this.projects.some(project => project.title.toLocaleLowerCase('uk-UA') === normalized)) return null
      const project = { id: `project-${this.nextProjectId++}`, title }
      this.projects.push(project)
      return project
    },
  },
})
