<template>
  <div id="app">
   <b-tabs content-class="mt-3">

        
 <router-view></router-view>

   

</b-tabs>

  </div>
</template>

<script>
  export default {
  
    data() {
      return {

      }
    },

    mounted () {

    let script1 = document.createElement('script')
    let script2 = document.createElement('script')
    let script3 = document.createElement('script')
    let script4 = document.createElement('script')
    let meta = document.createElement('meta')
    let link = document.createElement('link')

    link.setAttribute('rel',"stylesheet")
    link.setAttribute('href',"https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css")
    link.setAttribute('integrity',"sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk")
    link.setAttribute("crossorigin","anonymous")
    meta.setAttribute('name','viewport')
    meta.setAttribute('content',"width=device-width, initial-scale=1, shrink-to-fit=yes")
    script1.setAttribute('src', "https://unpkg.com/amazon-quicksight-embedding-sdk@1.0.17/dist/quicksight-embedding-js-sdk.min.js") // url from file goes here
    script2.setAttribute('src','https://code.jquery.com/jquery-3.5.1.min.js')
    script3.setAttribute('src','https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js')
    script3.setAttribute('integrity',"sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo")
    script3.setAttribute("crossorigin","anonymous")
    script4.setAttribute('src','https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js')
    script4.setAttribute('integrity',"sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI")
    script4.setAttribute("crossorigin","anonymous")
    document.head.appendChild(meta) 
    document.head.appendChild(link)
    document.head.appendChild(script1)
    document.head.appendChild(script2)
    document.head.appendChild(script3)
    document.head.appendChild(script4)
    
  }}

  
   </script>

<style scoped>

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #2c3e50;
  margin-top: 5%;
  margin-left: 10%;
  position:absolute;
  height: 100%;
  width: 80%;
}


</style>
