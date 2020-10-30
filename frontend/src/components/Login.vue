<template>
  <div class="login-form">
      <template v-if="user != null && user != 'null'">
          <span title="Logout"><a class="pointer" v-on:click="logout">{{ user }}</a></span>
      </template>
      <template v-if="user == null || user == 'null'">
        <a class="pointer" v-on:click="show">Login</a>
        <b-modal
        id="modal-login"
        ref="login-modal"
        title="login"
        @show="resetModal"
        @hidden="resetModal"
        @ok="handleOk"
        >
        <form ref="login-form" @submit.stop.prevent="handleSubmit">
            <b-form-group
            :state="loginState"
            invalid-feedback="Invalid input"
            >
            <b-form-input
                id="name-input"
                v-model="username"
                :state="loginState"
                placeholder="Username"
                required
            >Username </b-form-input>
            <b-form-input
                id="password-input"
                type="password"
                v-model="password"
                :state="loginState"
                placeholder="Password"
                required
            >Password </b-form-input>
            </b-form-group>
        </form>
        </b-modal>
    </template>
  </div>
</template>

<script>
export default {
  name: 'Login',
  props: ["user"],
  data() {
      return {
          username: '',
          password: '',
          loginState: null,
      }
  },
  methods: {
      show(){
          this.$bvModal.show('modal-login')
      },
      checkFormValidity() {
        const valid = this.$refs['login-form'].checkValidity()
        this.loginState = valid
        return valid
      },
      resetModal() {
        this.username = ''
        this.password = ''
        this.loginState = null
      },
      handleOk(bvModalEvt) {
        bvModalEvt.preventDefault()
        this.handleSubmit()
      },
      handleSubmit() {
        if (!this.checkFormValidity()) {
          return
        }
        this.$emit("do-login", {username: this.username, password: this.password})

        this.$nextTick(() => {
          this.$bvModal.hide('modal-login')
        })
      },
      logout(){
          this.$emit("do-logout")
      }
  }
}
</script>

<style scoped>
btn {
    border: 0;
    padding: 0;
}
.pointer {
    text-decoration: inherit;
    color: inherit;
    cursor: pointer;
}
</style>
