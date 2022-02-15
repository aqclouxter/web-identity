<template>
  <div>
    <b-card id="tab">
      <b-card-title id="title">Login</b-card-title>
      <b-form @submit="onSubmit" @reset="onReset" >
        <b-form-group
          class="userform"
          id="input-group-2"
          label="Username:"
          label-for="input-2"
        >
          <b-form-input
            id="input-2"
            v-model="form.username"
            placeholder="Enter username"
            class="userform"
            required
          ></b-form-input>
        </b-form-group>

        <b-form-group
          id="input-group-1"
          label="password:"
          label-for="input-1"
          class="userform"
          description="We'll never share your with anyone else."
        >
       
          <b-form-input
            id="input-1"
            v-model="form.password"
            type="password"
            placeholder="Enter password"
            class="userform"
            required
          ></b-form-input>
        </b-form-group>

        <p></p>
        <b-button id="button1" type="submit" variant="outline-primary"
          >Submit</b-button
        >
      </b-form>

    </b-card>
  </div>
</template>

<script>
import { CognitoUserPool, CognitoUser, AuthenticationDetails } from 'amazon-cognito-identity-js';
import APIURL  from "./constants.js";
import COGNITO_POOL_ID  from "./constants.js";
import COGNITO_POOL_URL  from "./constants.js";
import COGNITO_CLIENT_ID  from "./constants.js";
import AWS from 'aws-sdk';

export default {
  name: "login",
  data() {
    return {
      apiurl: APIURL["APIURL"],

      userPoolUrl:COGNITO_POOL_URL['COGNITO_POOL_URL'],
      userPool:null,
      usePoolData:null,
      form: {
        password: "",
        username: ""
      }
    };
  },
  created(){
    var poolData = {
        UserPoolId:COGNITO_POOL_ID['COGNITO_POOL_ID'],
        ClientId:COGNITO_CLIENT_ID['COGNITO_CLIENT_ID'],

        }
    this.usePoolData = poolData
    this.userPool = new CognitoUserPool(poolData);
  },
  methods: {

    onSubmit(event) {
      event.preventDefault();
      console.log(this.form)
      var authenticationData = {
        Username: this.form.username,
        Password: this.form.password

      }
      var authenticationDetails = new AuthenticationDetails( authenticationData );
      var userData = {
        Username: this.form.username,
        Pool: this.userPool
        };
      var cognitoUser = new CognitoUser(userData);
      var _router = this.$router
      cognitoUser.authenticateUser(authenticationDetails, {
        onSuccess: function(result) {
          AWS.config.region = 'us-east-1';
          AWS.config.credentials = new AWS.CognitoIdentityCredentials({
            IdentityPoolId: 'us-east-1:fe88ecb0-0eae-464a-9903-f7e828da0cda', 
            Logins: {
              'cognito-idp.us-east-1.amazonaws.com/us-east-1_Fum8K3y6T': result
              .getIdToken()
              .getJwtToken(),
              },
              });
          AWS.config.credentials.refresh(error => {
            if (error) {
              console.error(error);
              } else {
                console.log('Successfully logged!');
                _router.push({path:'dashboards'})

                }
                });
              
                },
        onFailure: function(err) {
          alert(err.message || JSON.stringify(err));
          },
          });
          },
        onReset(event) {
          event.preventDefault();
          // Reset our form values
          this.form.email = "";
          this.form.username = "";
          // Trick to reset/clear native browser form validation state
          this.show = false;
          this.$nextTick(() => {
            this.show = true;
            });
          }
            },
            };
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#title{
  position:relative;
  left: 40%;
}
#tab {
  position: relative;
  width: 30%;
  left: 35%;
  top: 25%;
}
.userform {
  position: relative;

}
#button1 {
  position: relative;
  top: 55%;
  width: 30%;
  left: 35%;
}

</style>
