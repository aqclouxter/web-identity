<template>
  <div >
  

    <b-tab title="Groups">
       <p></p> 
    <b-form-input v-model="text" placeholder="Enter group name"></b-form-input>
    <p></p>
    <b-form-input v-model="description" placeholder="Enter group description"></b-form-input>
    <p></p>
    <b-button id="button1" variant="outline-primary" v-on:click="create_group">Create group</b-button>
   <p></p>
   <b-table 
   striped hover 
   :items="items"
    ref="table1"
    selectable
    select-mode="single"
    @row-clicked="rowSelected"
    primary-key="Name"
   
   ></b-table>
    <b-alert show variant="danger" v-if="row_selected === 1">
    <div class="mt-3 dashboards"><strong>you are about to delete  group <strong>"{{ delgroup }}",</strong> click delete button to continue or cancel to abort</strong></div>
    </b-alert>
   <b-button id="button1" v-if="row_selected === 1" variant="outline-danger" v-on:click="delete_group">delete</b-button>
   <p></p>
   <b-button id="button1" v-if="row_selected === 1" variant="outline-primary" v-on:click="cancel_delete">cancel</b-button>
   <p></p>
    <b-alert show variant="success" v-if="status === 201">
    <div class="mt-3 "><strong>group successfully created</strong></div>
    </b-alert>
    <b-alert show variant="success" v-if="status === 204">
    <div class="mt-3 dashboards"><strong>group succesfully delete</strong></div>
    </b-alert>
    </b-tab>
    

  </div>
</template>

<script>
 import axios from 'axios'
 import APIURL from './constants.js'
  export default {
    name: "groups",
    data() {
      return {
        componentKey:0,
        status:0,
        text:"",
        description:"",
        apiurl:APIURL['APIURL'],
        items: [],
        delgroup:"",
        row_selected:0,
        delindex:0

      }
    },
    mounted () {

    axios
      .get(this.apiurl+"/admin/groups")
      .then(response => (response["data"]["GroupList"].forEach(element => {
        console.log(element)
        this.items.push({Name: element["groupName"],members:element["member_list"]})
      })))
    
  },
  methods: {
    create_group: function(){
    axios
      .post(this.apiurl+"/admin/groups",{"group_name":this.text,"description":this.description})
      .then(response => ( this.status = response["data"].Status, console.log(response["data"].Status),this.items.push({"Name":this.text,"description":this.description}),this.text="",this.description="" ))

      
    },
    delete_group: function(){
    axios
      .delete(this.apiurl+"/admin/groups/" + this.delgroup)
      .then(response => ( this.status=response.status))
      this.row_selected=0
      this.items.splice(this.delindex,1)
      
      

    },
    rowSelected(record,index){

      this.delindex = index
      this.delgroup=record["Name"]
      this.row_selected=1
      this.status=0
    },
    cancel_delete: function(){
      this.delgroup=""
      this.row_selected=0
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
</style>