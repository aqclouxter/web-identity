<template>
  <div id="tag">
   

</div>
</template>

<script>

 import AWS from 'aws-sdk';

  export default {
    
    mounted () {
          
this.democlick();

      
  }
  ,
  methods: {
    democlick(){
      let params = {
                  Bucket: "web-identity-demo"
                }
      var s3 = new AWS.S3();
      
      s3.listObjects(params, function(err, data) {
        if (err) {console.log(err, err.stack);} // an error occurred
        else { console.log(data.Contents),  document.getElementById("tag").innerHTML="<table><th style='padding:30px;'>Key</th><th>Last Modified</th><tr><td style='padding:30px;'>"+ data.Contents[0].Key +"</td><td > "+ data.Contents[0].LastModified +"</td></tr></table>"; }
      });
  }
  }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.dashboards {
  position:relative;
  top:25%;
  width: 100%;
}
#button1 {
  position:relative;
  top:55%;
  width: 100%;
}
#logout {
  position: absolute;
  right: 0%
}
#progress {
  position: absolute;
  z-index: 100;
  top: 20%;
  left:40%;
  backdrop-filter: blur(5px);

}
</style>
