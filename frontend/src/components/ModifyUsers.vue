<template>
  <div class="modify-user">
    <a v-on:click="show">Modify User</a>
    <b-modal
      id="modal-modify-user"
      ref="modal"
      title="Modify User"
      @show="resetModal"
      @hidden="hideModal"
      @ok="handleOk"
    >
        <b-list-group>
            <b-list-group-item class="pointer" v-on:click="select(u)" v-for="u in users" :key="u">
                {{ u }}
            </b-list-group-item>
        </b-list-group>
        <form class="mt-5" ref="form" @submit.stop.prevent="handleSubmit">
            <b-form-group
            :state="userState"
            >
            <b-form-radio-group class="mt-1"
                id="radio-group-1"
                v-model="selected"
                :options="options"
                name="radio-options"
            ></b-form-radio-group>
            <b-form-input class="mt-1"
                user="user-input"
                placeholder="username"
                v-model="user"
                :state="userState"
                required
            ></b-form-input>
            <template v-if="selected == 'Reset Password' || selected == 'Add User'">
            <b-form-input class="mt-1"
                password="password-input"
                placeholder="set password"
                type="password"
                v-model="password"
                :state="userState"
            ></b-form-input>
            </template>
            </b-form-group>
        </form>
    </b-modal>
  </div>
</template>

<script>
import Api from '@/services/api';

export default {
  name: 'ModifyUsers',
  props: {
  },
  data() {
      return {
          users: null,
          user: '',
          password: '',
          userState: null,
          selected: 'Reset Password',
          options:[
              { text: "Reset Password", value: 'Reset Password'},
              { text: "Add", value: 'Add User'},
              { text: "Remove", value: 'Remove User'}
          ]
      }
  },
  methods: {
      show(){
          this.getUsers();
          this.$bvModal.show('modal-modify-user');
          this.$emit("pause-timer", true)
      },
      checkFormValidity() {
        const valid = this.$refs.form.checkValidity();
        this.userState = valid;
        return valid
      },
      resetModal() {
        this.users = null;
        this.user = '';
        this.password = '';
        this.selected = 'Reset Password';
        this.userState = null;
      },
      hideModal(){
        this.$emit("pause-timer", false)
        this.resetModal()
      },
      handleOk(bvModalEvt) {
        bvModalEvt.preventDefault();
        this.handleSubmit();
      },
      handleSubmit() {
        if (!this.checkFormValidity()) {
          return
        }
        this.$emit("modify-user", {username: this.user, modify: this.selected, password: this.password})

        this.$nextTick(() => {
          this.$bvModal.hide('modal-modify-user')
        })
      },
      select(data){
          this.user = data
      },
      async getUsers(){
          let data = (await Api.getUsers()).data
          this.users = data
      }
  }
}
</script>

<style scoped>
btn {
    border: 0;
    padding: 0;
}
</style>
