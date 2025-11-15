const app = Vue.createApp({
  data() {
    return {
      title: "Good deeds",
      author: "Tirus Gibson",
      age: 46
    }
  },
  methods:{
    data2(){
      this.title2="Good deeds2"
    }
  }
});
app.mount("#app")