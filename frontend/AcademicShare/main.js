import Vue from 'vue'
import App from './App'
import SearchBar from './components/SearchBar.vue'
import AppHeader from './components/AppHeader.vue'
import Footer from './components/Footer.vue'
import Resource from './components/Resource.vue'
import ResourceFooter from './components/ResourceFooter.vue'
import Row from './components/oveui-layout/row/row.vue'
import oCol from './components/oveui-layout/o-col/o-col.vue'
import CommentCard from './components/CommentCard.vue'

Vue.config.productionTip = false

App.mpType = 'app'

const app = new Vue({
    ...App
})
const { windowWidth, windowHeight } = uni.getSystemInfoSync();	
app.$mount()
Vue.component('SearchBar',SearchBar)
Vue.component('AppHeader',AppHeader)
Vue.component('Footer',Footer)
Vue.component('Resource',Resource)
Vue.component('ResourceFooter',ResourceFooter)
Vue.component('Row',Row)
Vue.component('oCol',oCol)
Vue.component('CommentCard',CommentCard)
