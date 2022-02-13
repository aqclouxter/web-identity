<template>
  <div>
    <b-card id="tab">
      <b-card-title id="title">Login</b-card-title>
      <b-form @submit="onSubmit" @reset="onReset" v-if="show">
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

      <h2 v-if="show2">Change Password</h2>
      <b-form @submit="onSubmit2" @reset="onReset2" v-if="show2">
        <b-form-group
          class="userform"
          id="input-group-3"
          label="a Username:"
          label-for="input-3"
        >
          <b-form-input
            id="input-3"
            v-model="form2.username"
            placeholder="Enter username"
            class="userform"
            required
          ></b-form-input>
        </b-form-group>

        <b-form-group
          id="input-group-4"
          label="password:"
          label-for="input-4"
          class="userform"
          description="Enter new password"
        >
          <b-form-input
            id="input-4"
            v-model="form2.password"
            type="password"
            placeholder="Enter new password"
            class="userform"
            required
          >
          </b-form-input>

          <b-form-group
            id="input-group-5"
            label="Session id:"
            label-for="input-5"
            class="userform"
            description="Session id"
          ></b-form-group>
          <b-form-input
            id="input-5"
            v-model="form2.session"
            placeholder="Enter new password"
            class="userform"
            disabled
          ></b-form-input>
        </b-form-group>


        <p></p>
        <b-button id="button1" type="submit" variant="outline-primary"
          >Reset password</b-button
        >
      </b-form>
    </b-card>
  </div>
</template>

<script>
import axios from "axios";
import APIURL from "./constants.js";
import COGNITO_POOL_ID from "./constants.js";
export default {
  name: "login",
  data() {
    return {
      apiurl: APIURL["APIURL"],
      form: {
        password: "",
        username: "",
        pool: COGNITO_POOL_ID['POOL_ID1']
      },
      show: true,
      show2: false,
      form2: {
        password: "",
        username: "",
        session: "",
        pool: ""
      },
    };
  },

  methods: {
    onSubmit(event) {
      event.preventDefault();
      console.log(this.form)
      axios.post(this.apiurl + "/login", this.form).then((response) => {
        if (response["data"]["idToken"]) {
          this.$router.push({
            path: "dashboards",
            query: { openIdToken: response["data"]["idToken"], 
                     poolId: response["data"]["poolId"], 
                     clientId: response["data"]["clientId"],
                     domainUrl: response["data"]["domainUrl"]
                     },
          });
        } else {

            this.show2 = true;
            this.show = false;
            this.form2.username = this.form.username;
            this.form2.session = response["data"]["Session"];
            this.form2.pool = this.form.pool
            
          
        }
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
    },
    onSubmit2(event) {
      event.preventDefault();
      axios
        .post(this.apiurl + "/login", this.form2)
        .then((response) => console.log(response));
          this.show2 = false;
            this.show = true;
            this.form.username = this.form2.username;
    },
    onReset2(event) {
      event.preventDefault();
      // Reset our form values
      this.form.email = "";
      this.form.username = "";
      this.form.checked = [];
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
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
#button2 {
  position: relative;
  top: 55%;
  width: 30%;
  left: 35%;
}
</style>
