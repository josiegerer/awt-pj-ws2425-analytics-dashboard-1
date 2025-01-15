import { createRouter, createWebHistory } from 'vue-router';
import OverallView from './views/OverallView.vue';
import PerformanceView from './views/PerformanceView.vue';
import EngagementView from './views/EngagementView.vue';
import EducatorDashboard from './views/EducatorDashboard.vue';

const routes = [
  { path: '/', redirect: '/overall' },
  { path: '/overall', name: 'Overall', component: OverallView },
  { path: '/performance', name: 'Performance', component: PerformanceView },
  { path: '/engagement', name: 'Engagement', component: EngagementView },
  {path: '/educator-dashboard', name: 'EducatorDashboard', component: EducatorDashboard}
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

