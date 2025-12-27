import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import NotFoundView from '../views/NotFoundView.vue'

import TasksLayout from '../views/tasks/TasksLayout.vue'
import TaskListView from '../views/tasks/TaskListView.vue'
import TaskNewView from '../views/tasks/TaskNewView.vue'
import TaskEditView from '../views/tasks/TaskEditView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/tasks',
    component: TasksLayout,
    children: [
      {
        path: '',
        name: 'tasks',
        component: TaskListView,
      },
      {
        path: 'new',
        name: 'task-new',
        component: TaskNewView,
      },
      {
        path: ':id/edit',
        name: 'task-edit',
        component: TaskEditView,
        props: true,
      },
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFoundView,
  },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})
