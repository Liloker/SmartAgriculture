import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

/* Layout */
import Layout from "../views/layout/Layout";

/**
 * hidden: true                   if `hidden:true` will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu, whatever its child routes length
 *                                if not set alwaysShow, only more than one route under the children
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noredirect           if `redirect:noredirect` will no redirct in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    title: 'title'               the name show in submenu and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar,
  }
 **/
export const constantRouterMap = [{
    path: "/login",
    component: () => import("@/views/login/index"),
    hidden: true
  },
  {
    path: "/404",
    component: () => import("@/views/404"),
    hidden: true
  },
  {
    path: "",
    component: Layout,
    name: "member",
    redirect: "/index",
    meta: {
      title: "首页大屏",
      icon: "product"
    },
    children: [
      {
        path: "index",
        name: "member",
        component: () => import("@/views/charts/index"),
        meta: {
          title: "首页大屏",
          icon: "Neirongguanli"
        }
      }
    ]
  },
  {
    path: "/sensor",
    component: Layout,
    name: "sensor",
    meta: {
      title: "传感器管理",
      icon: "eye"
    },
    children: [{
        path: "",
        name: "sensor-index",
        component: () => import("@/views/sensor/index"),
        meta: {
          title: "传感器管理",
          icon: "yuanqu"
        }
      }
    ]
  },
  {
    path: "/scan",
    component: Layout,
    name: "scan",
    meta: {
      title: "病虫害识别",
      icon: "eye"
    },
    children: [{
        path: "",
        name: "scan-index",
        component: () => import("@/views/scan/index"),
        meta: {
          title: "病虫害识别",
          icon: "yuanqu"
        }
      }
    ]
  },
  {
    path: "/greenhouse",
    component: Layout,
    name: "greenhouse",
    meta: {
      title: "大棚管理",
      icon: "eye"
    },
    children: [{
        path: "",
        name: "greenhouse-index",
        component: () => import("@/views/greenhouse/index"),
        meta: {
          title: "大棚管理",
          icon: "yuanqu"
        }
      }
    ]
  },
  {
    path: "/plant",
    component: Layout,
    name: "plant",
    meta: {
      title: "大棚管理",
      icon: "eye"
    },
    children: [{
        path: "",
        name: "plant-index",
        component: () => import("@/views/plant/index"),
        meta: {
          title: "农产品种植物管理",
          icon: "yuanqu"
        }
      },
      {
        path: "productionCycle",
        name: "productionCycle-index",
        component: () => import("@/views/productionCycle/index"),
        meta: {
          title: "生产周期管理",
          icon: "yuanqu"
        },
        hidden: true
      }
    ]
  },
  {
    path: "*",
    redirect: "/404",
    hidden: true
  }
];

export default new Router({
  // mode: 'history', //后端支持可开
  scrollBehavior: () => ({
    y: 0
  }),
  routes: constantRouterMap
});