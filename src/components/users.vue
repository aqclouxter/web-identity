<template>
  <div >
  

    <b-tab title="Users">

    <b-form @submit="onSubmit" @reset="onReset" v-if="show">


      <b-form-group class="userform" id="input-group-2" label="a Username:" label-for="input-2">
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
        label="Email address:"
        label-for="input-1"
        class="userform"
        description="We'll never share your email with anyone else."
      >
        <b-form-input
          id="input-1"
          v-model="form.email"
          type="email"
          placeholder="Enter email"
          class="userform"
          required
        ></b-form-input>
      </b-form-group>

        <b-form-group id="input-group-6" label="POOL_ID:" class="userform" label-for="input-6">
        <b-form-select
          id="input-6"
          v-model="form.pool"
          :options="pools"
          class="userform"
          :select-size="4"
          required
        ></b-form-select>
      </b-form-group>

      <b-form-group id="input-group-3" label="group:" class="userform" label-for="input-3">
        <b-form-select
          id="input-3"
          v-model="form.group_name"
          :options="group"
          class="userform"
          :select-size="4"
          required
        ></b-form-select>
      </b-form-group>
           <b-form-group id="input-group-4" label="organization:" class="userform" label-for="input-4">
        <b-form-select
          id="input-4"
          v-model="form.organization_id"
          :options="organization"
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
      <b-alert show variant="danger" v-if="status !== 201 && status !== 0">
    <div class="mt-3 dashboards"><strong>there was an error creating user</strong></div>
    </b-alert>

    </b-tab>
    

  </div>
</template>

<script>
 import axios from 'axios'
 import APIURL from './constants.js'
 import COGNITO_POOLS from "./constants.js";
export default {
     name: "users",
    data() {
      return {
        apiurl:APIURL['APIURL'],
        pools: [{text:'pool_id1',value:COGNITO_POOLS['COGNITO_POOLS']['POOL_ID1']},
               {text:'pool_id2',value:COGNITO_POOLS['COGNITO_POOLS']['POOL_ID2']} ],
        form: {
          email: '',
          username: '',
          group_name: '',
          organization_id: '',
          pool:''
        
        },
        group: [],
        organization: [],
        show: true,
        status:0
      }
    },
    mounted(){
    axios
      .get(this.apiurl+"/admin/groups")
      .then(response => (response["data"]["GroupList"].forEach(element => {
        console.log(element)
        this.group.push({value: element["groupName"],text: element["groupName"]})
      })))
    axios
      .get(this.apiurl+"/admin/organizations")
      .then(response => (response["data"].forEach(element => {

        this.organization.push({ text: element["name"], value: element["organization_id"] })
      })))

    },
    methods: {
      onSubmit(event) {
        event.preventDefault()
    axios
      .post(this.apiurl+"/admin/users",this.form)
      .then(response => {
        if(response.status===201){
          this.$router.push({path:"login"}) 
          }
          else{
          this.status = 400
          }
          })
      
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
</style>