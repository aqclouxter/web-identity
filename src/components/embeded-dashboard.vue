<template>
  <div >
  <b-form @submit="onSubmit" @reset="onReset" v-if="show">
        <b-form-group id="input-group-3" label="dashboards:" class="userform" label-for="input-3">
        <b-form-select
          id="input-3"
          v-model="form.dashboard"
          :options="Dashboards"
          class="userform"
          :select-size="4"
          required
        ></b-form-select>
      </b-form-group>
            <p></p> 
      <b-button id="button1" type="submit" variant="outline-primary">Submit</b-button>
      <b-button id="button2" type="reset" variant="outline-secondary">Reset</b-button>
  </b-form>
  <p></p>
  <div id="DashboardEmbedUrl">
  </div>
  </div >
  
</template>


<script>


 import axios from 'axios'
 import APIURL   from './constants.js' 
 import QSURL   from './constants.js'
 import COGNITO_DOMAIN_URL from './constants.js'
 import COGNITO_CLIENT_ID from './constants.js'
 import * as QuickSightEmbedding from 'amazon-quicksight-embedding-sdk'
  export default {
    name:"embeded",
    data() {

      return {
        apiGatewayUrl:QSURL["QSURL"],
        staticPageUrl:QSURL["QSURL"],
        cognitoDomainUrl:COGNITO_DOMAIN_URL["COGNITO_DOMAIN_URL"],
        cognitoClientId:COGNITO_CLIENT_ID["COGNITO_CLIENT_ID"],
        organizationId:'<organizationId>',
        cognitoPoolId:"",
        dashboardInitialLoad:true,
        dashboard:'',
        session:'',
        timerId:'',
        debugMode: false,
        status:0,
        apiurl: APIURL['APIURL'],
        qsurl: QSURL["QSURL"],
        selected1: [], // Array reference
        options1: [],        
        selected2: [], // Array reference
        options2: [],
        openIdToken:'',
        Dashboards:[],
        show:true,
        
        form:{
            dashboardUrl:"",
            dashboard:""
        }
      }
    },


    mounted () {
    this.cognitoDomainUrl = this.$route.query.domainUrl
    this.cognitoClientId = this.$route.query.clientId
    this.cognitoPoolId = this.$route.query.poolId
    this.openIdToken = this.$route.query.openIdToken
    var timestamp =  new Date().getTime() 
    this.quickSightInfo(timestamp, this.openIdToken, this.cognitoDomainUrl, this.cognitoClientId)
  },
    methods: {
      onSubmit(event) {
        event.preventDefault()
        console.log(this.form.dashboardUrl)
        console.log(this.form.dashboard)
        this.selectDashboard(this.form.dashboard)
      },
      onReset(event) {
        event.preventDefault()
        // Reset our form values
        this.form.email = ''
        this.form.username = ''
        this.form.group_name = null
        this.form.organization_id = null
        this.form.checked = []
        // Trick to reset/clear native browser form validation state
        this.show = false
        this.$nextTick(() => {
          this.show = true
        })
      },
    embedQuickSight(entity, embedDiv, embedUrl) {
        
        var containerDiv = document.getElementById(embedDiv);
        var params = {
                url: embedUrl,
                container: containerDiv,
                width:"100%",
                height:"100%",
                undoRedoDisabled: true, 
                resetDisabled: true,
        };
        console.log(params)
        if (entity == 'Dashboard'){
         this.dashboard = QuickSightEmbedding.embedDashboard(params);         
        }
        else {
          this.session = QuickSightEmbedding.embedSession(params);         
        }
      },
      quickSightInfo(timestamp, idToken, domainUrl, clientId){
         axios
      .get(this.qsurl+"?mode=getDashboardList&openIdToken=" + idToken +"&timestamp=" + timestamp + "&domainUrl=" + domainUrl + "&clientId=" + clientId)
      .then(response => {
          console.log("in dashboard list "+response["data"])
          this.setCookie('QSEmbedDemo','{"openIdToken":"'+ idToken +'", "expiryTs":'+response["data"]["expiryTs"],parseInt(response["data"]["expiryTs"] - Date.now()/1000));
        //   this.checkSessionDuration()
        //   this.timerId = setInterval(function(){this.checkSessionDuration();},60000);
          for(var dashboard in response["data"]["response"]["Dashboards"] ){
              var dash = response["data"]["response"]["Dashboards"][dashboard]
              this.Dashboards.push({text:dash["Name"],value:dash["DashboardId"]})            
          }
          })
    axios
         .get(this.qsurl+"?mode=getUrl&openIdToken=" + idToken + "&timestamp=" + timestamp + "&domainUrl=" + domainUrl + "&clientId=" + clientId )
         .then(response =>{
             console.log("in get url"+response["data"])
           this.form.dashboardUrl = response["data"]["response"]["DashboardEmbedUrl"]
           this.embedQuickSight('Dashboard', 'DashboardEmbedUrl', this.form.dashboardUrl)
           this.organizationId = response["data"]["organization_id"]    
         })
      },
        selectDashboard(dashboardId){   
        if (dashboardId != 'non-existent-id')
        {
          var options = {
                dashboardId: dashboardId,
                parameters:{
                  organizationId: this.organizationId
                }
            };
          console.log(options)
          this.dashboard.navigateToDashboard(options);
        }
      },
        setCookie(name, value) {
        
        document.cookie = name + "=" + value +"; Max-Age=3600; SameSite=Strict";
      },
        getCookie(name) {
        
        var v = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
        return v ? v[2] : null;
      },
        getCookieField(fieldName) {
       
        var cookie = this.getCookie('QSEmbedDemo');
        if (cookie)
        {
          var fieldValue = JSON.parse(cookie)[fieldName];
          return fieldValue
        }
      },
        signOut(){    
        this.setCookie('QSEmbedDemo', '');
        clearInterval(this.timerId);   
      },
        checkSessionDuration(){
        var expiryTs = this.getCookieField('expiryTs')
        if (expiryTs)
        {
          var sessionDuration = parseInt((expiryTs - (Date.now()/1000) )/60 );
          sessionDuration = sessionDuration >= 0 ? sessionDuration : 0 ;
          
          if (sessionDuration == 0)
          {
            this.signOut();
          }
        }
        else
        {
          this.signOut();
        }
      } 
    }

  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.userform {
  position:relative;
  top:25%;
  width: 100%;
}
#button1 {
  position:relative;
  top:55%;
  width: 100%;
}
#button2 {
  position:relative;
  top:55%;
  width: 100%;
}
#DashboardEmbedUrl {
 position:relative;
 top: 6%;
 height: 500px;
}
</style>

