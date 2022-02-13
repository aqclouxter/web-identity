<template>
  <div >
    
    <b-btn id="logout" class="btn btn-default" @click="logout()" v-if="apiToken!==null" >logout</b-btn>
    
    <b-input-group-append>
    <b-btn variant="outline-secondary" v-b-modal.modal-1>+</b-btn>
  </b-input-group-append>
  <b-alert variant="primary" show>Nice DCV may take up to 2 minutes to be accessible after instance is ready</b-alert>
  <b-table striped hover :items="items" class="dashboard" :fields="fields" fixed>
        <template #cell(actions)="data">
      <button class="btn btn-default" @click="send_item(data.item.instance_id, data.item.region)" :ref="'btn' + data.index" v-if="data.item.instance_state=='Ready'" v-b-modal.modal-2><font-awesome-icon icon="trash" /></button>
      <button class="btn btn-default"  v-if="data.item.instance_state!=='Ready'" disabled><font-awesome-icon icon="trash" /></button>
      <a class="btn btn-default" v-if="data.item.instance_state=='Ready'"  :href="'https://'+data.item.public_dns+':8443'" > <font-awesome-icon icon="link" /> </a>
      <a class="btn btn-default" v-if="data.item.instance_state!=='Ready'"  disabled > <font-awesome-icon icon="link" /> </a>
     <a class="btn btn-default" v-if="data.item.instance_state=='Ready'" @click="copy_url('https://'+data.item.public_dns+':8443')" > <font-awesome-icon icon="copy" /> </a>
     <a class="btn btn-default"  v-if="data.item.instance_state!=='Ready'"  disabled> <font-awesome-icon icon="copy" /> </a>
      
    </template>
   
  

  



  </b-table>
  <vue-ellipse-progress id="progress" 
  v-if="prog===true"
  progress="100"
  :animation="time_prog"
  
  />
<div>
 
  <b-modal id="modal-2" title="Delete Instance">
      <template #modal-footer>

      <button class="btn btn-primary" @click="delete_instance(delete_item)" >confirm</button>
      <button class="btn btn-danger" @click="cancel_delete()" >cancel</button>
      
        
      </template>



  </b-modal>
  <b-modal id="modal-1" title="Run Instance">
    <template #modal-footer>
     <b-form @submit="onSubmit" @reset="onReset" v-if="show" class="container">

    <b-form-group id="input-group-2" label="region:" label-for="input-2">
        <b-form-select
          id="input-2"
          v-model="form.region"
          :options="regions"
          @change="get_amis()"
          required
        ></b-form-select>
        </b-form-group>
      
      <p><small><strong>Instance Type:</strong> g4dn.xlarge 4cpus, 16 gb RAM  </small></p>
      <p><small><strong>Storage:</strong> 50 GIB in ebs volume</small></p>
      <p><small><strong>Description:</strong> G4dn instances feature NVIDIA T4 GPUs and custom Intel Cascade Lake CPUs, bringing  high performance to graphics-intensive applications including remote workstations, game streaming, and graphics rendering. </small></p>
<hr>
      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>

    </b-form>
    </template>
  </b-modal>
</div>
  </div>
</template>

<script>

 import axios from 'axios'
 import APIURL from './constants.js'

  export default {
    
    data() {
      return {
        apiurl:APIURL['APIURL'],
        polling : '',
        apiToken: '',
        status:"",
        items: [],
        delete_item:"",
        region:"",
        fields: ["instance_id", "instance_state", "instance_type", "time","user","region", "actions"],
        types: [{ text: 'Select One', value: null },'g4dn.xlarge'],
        amis:[{ text: 'Select One', value: null }],
        tmp:'',
        name:[],
        des: '',
        show: true,
        prog:false,
        t_prog:0,
        time_prog:"",
        regions:['us-east-1','us-west-2'],
        form: {
          type: '',
          ami: '',
          region:''
        },

      
      }
    },
    mounted () {
    this.apiToken = this.$route.query.openIdToken
    console.log(this.apiToken)
    this.pollData()
    axios
      .get(this.apiurl+"/dashboard/amis")
      .then(response => { this.tmp=response["data"] })
  },
  methods: {
	pollData () {
    axios
      .get(this.apiurl+"/dashboard",{ headers: { Authorization: 'Bearer ' + this.apiToken }})
      .then(response => { this.items=response["data"], console.log(this.items)  })
		this.polling = setInterval(() => {
		axios
      .get(this.apiurl+"/dashboard",{ headers: { Authorization: 'Bearer ' + this.apiToken }})
      .then(response => { this.items=response["data"], console.log(this.items) })
		}, 3000)
	},
    delete_instance: function(instance_id){
    axios
     .delete(this.apiurl + "/dashboard?instance_id=" + instance_id +"&region=" + this.region, { headers: { Authorization: 'Bearer ' + this.apiToken }} ).then(response =>{console.log(response),this.$bvModal.hide('modal-2')})
    },
    onSubmit: function(event){
    setTimeout(() => {  this.$bvModal.hide('modal-1') }, 1000)
      console.log(this.form)

      if (this.form.region === "us-east-1"){
          this.time_prog = "default 180000 0"
          this.t_prog = 180000
      } else {
        this.t_prog = 125000
         this.time_prog = "default 125000 0"
      }
      console.log(this.time_prog)
      if (event) {
      event.preventDefault()
    }
      axios
       .post(this.apiurl + "/dashboard", this.form, { headers: { Authorization: 'Bearer ' + this.apiToken }} ).then(response => {this.status = response.status, this.prog=true, setTimeout(() => {  this.prog=false }, this.t_prog) })

    },
    onReset: function(){
      this.ami = ''
      this.type = ''

    },
    send_item: function(instance_id,region){
      this.delete_item = instance_id
      this.region = region
    },
    cancel_delete: function(){
      this.$bvModal.hide('modal-2')
    },
    logout: function(){
      this.apiToken=null
      this.$router.push({path:"/"})
    },
    get_amis: function(){
      console.log(this.form.region)
      console.log(this.amis)
      this.amis = [{ text: 'Select One', value: null }]
      for(var am in this.tmp){
        if (this.tmp[am][this.form.region] !== undefined){
          for (var re in this.tmp[am][this.form.region]){
        this.amis.push({text: this.tmp[am][this.form.region][re]['id'], value: this.tmp[am][this.form.region][re]['id']})
        this.name.push({id:this.tmp[am][this.form.region][re]['id'],name:this.tmp[am][this.form.region][re]['name']})
          }
        }
      }

    },
    get_name: function(){
      this.des=''
      for(var am in this.name){
        console.log(this.name[am]['id'])
        console.log(this.form.ami)
        if (this.form.ami == this.name[am]['id']){
         this.des = this.name[am]['name']
         console.log(this.des)
        }
      }
      
    },
    copy_url: function(url) {
     
        navigator.clipboard.writeText(url)
    }
},
beforeDestroy () {
	clearInterval(this.polling)
},
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
