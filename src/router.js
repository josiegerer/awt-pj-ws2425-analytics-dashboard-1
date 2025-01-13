import { createRouter, createWebHistory } from 'vue-router';
import OverallView from './views/OverallView.vue';
import PerformanceView from './views/PerformanceView.vue';
import EngagementView from './views/EngagementView.vue';

const routes = [
  { path: '/', redirect: '/overall' },
  { path: '/overall', name: 'Overall', component: OverallView },
  { path: '/performance', name: 'Performance', component: PerformanceView },
  { path: '/engagement', name: 'Engagement', component: EngagementView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

