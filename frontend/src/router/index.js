import { createRouter, createWebHistory } from 'vue-router';
import OverallView from '../views/OverallView.vue';
import PerformanceView from '../views/PerformanceView.vue';
import EngagementView from '../views/EngagementView.vue';
import AdminDashboard from '../views/AdminDashboard.vue';
import EducatorDashboard from '../views/EducatorDashboard.vue';

const routes = [
  {
    path: '/',
    redirect: '/overall',
  },
  {
    path: '/overall',
    name: 'Overall',
    component: OverallView,
  },
  {
    path: '/performance',
    name: 'Performance',
    component: PerformanceView,
  },
  {
    path: '/engagement',
    name: 'Engagement',
    component: EngagementView,
  },
  {
    path: '/admin-dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
  },
  {
    path: '/educator-dashboard',
    name: 'EducatorDashboard',
    component: EducatorDashboard,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
