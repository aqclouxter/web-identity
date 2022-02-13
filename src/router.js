import Vue from "vue";
import VueRouter from 'vue-router'
import dashboard from "./components/dashboard";
import login from "./components/login";

    
Vue.use(VueRouter)

const routes = [
    {
      path: "/dashboards",
      name: "dashboards",
      component: dashboard
    },
    {
        path: '/',
        redirect: '/login'
      },
      {
          path: '/login',
          name: "login",
          component: login
        }

  ];

const router = new VueRouter({
    mode: "history",
    routes
  });
  
  export default router;