import './main.css'

import {createApp} from 'vue'
import App from './App.vue'
import {createRouter, createWebHistory} from "vue-router";
import TransformAction from "@/components/actions/TransformAction.vue";
import FilterAction from "@/components/actions/FilterAction.vue";
import ExperimentAction from "@/components/actions/ExperimentAction.vue";
import NoAction from "@/components/actions/NoAction.vue";

const routes = [{
    path: "/",
    components: {
        default: NoAction
    }
}, {
    path: "/transform",
    props: true,
    components: {
        default: TransformAction
    }
}, {
    path: "/filter",
    props: true,
    components: {
        default: FilterAction
    }
}, {
    path: "/experiment",
    props: true,
    components: {
        default: ExperimentAction
    }
}];

const router = createRouter({
    history: createWebHistory(), routes,
});

createApp(App)
    .use(router)
    .mount('#app')
