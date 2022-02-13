<template>
  <div >
    <b-tab title="Organizations">
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group class="userform" id="input-group-2" label="a organization name:" label-for="input-2">
        <b-form-input
          id="input-2"
          v-model="form.name"
          placeholder="Enter organization name"
          class="userform"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="input-group-1"
        label="Organization Email address:"
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
            <b-form-group class="userform" id="input-group-3" label="a organization description:" label-for="input-3">
        <b-form-input
          id="input-3"
          v-model="form.description"
          placeholder="Enter organization description"
          class="userform"
          required
        ></b-form-input>
      </b-form-group>
    <b-form-group class="userform" id="input-group-4" label="a organization id:" label-for="input-4">
        <b-form-input
          id="input-3"
          v-model="form.organization_id"
          placeholder="Enter organization id"
          class="userform"
          required
        ></b-form-input>
      </b-form-group>

      <p></p>
      <b-button id="button1" type="submit" variant="outline-primary">Submit</b-button>
      <b-button id="button2" type="reset" variant="outline-secondary">Reset</b-button>
    </b-form>
       <p></p>
   <b-table 
   striped hover 
   :items="items"
    ref="table1"
    selectable
    select-mode="single"
    primary-key="Name"
   
   ></b-table>

    </b-tab>
    

  </div>
</template>

<script>
 import axios from 'axios'
 import APIURL from './constants.js'
export default {
    name: "organizations",
    data() {
      return {
        items:[],
        apiurl:APIURL['APIURL'],
        form: {
          email: '',
          name: '',
          id: '',
          description: ''
        },
        show: true
      }
    },mounted (){
    axios
      .get(this.apiurl+"/admin/organizations")
      .then(response => (response["data"].forEach(element => {
        console.log(element)
        this.items.push({Name: element["name"], Description: element["description"],Email: element["email"], Id: element["organization_id"] })
      })))
      
    },
    methods: {
      onSubmit(event) {
        event.preventDefault()
    axios
      .post(this.apiurl+"/admin/organizations",this.form)
      .then(response => (console.log(response),this.$router.go() ))
      
      },
      onReset(event) {
        event.preventDefault()
        // Reset our form values
        this.form.email = ''
        this.form.name = ''
        this.form.group = null
        this.form.organization = null
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