<template>
  <div class="login-form">
      <template v-if="user != null && user != 'null'">
          <span title="Logout"><a v-on:click="logout">{{ user }}</a></span>
      </template>
      <template v-if="user == null || user == 'null'">
        <a v-on:click="show">Login</a>
        <b-modal
        id="modal-login"
        ref="login-modal"
        title="Login"
        @show="resetModal"
        @hidden="hideModal"
        @ok="handleOk"
        >
        <form ref="login-form" @submit="handleSubmit">
            <b-form-group
            :state="loginState"
            invalid-feedback="Invalid input"
            >
            <b-form-input class="mt-1"
                id="name-input"
                v-model="username"
                :state="loginState"
                placeholder="Username"
                @keydown.enter.native="handleSubmit"
                required
            >Username </b-form-input>
            <b-form-input class="mt-1"
                id="password-input"
                type="password"
                v-model="password"
                :state="loginState"
                @keydown.enter.native="handleSubmit"
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
        this.$bvModal.show('modal-login');
        this.$emit("pause-timer", true);
      },
      checkFormValidity() {
        const valid = this.$refs['login-form'].checkValidity();
        this.loginState = valid;
        return valid
      },
      hideModal(){
        this.$emit("pause-timer", false);
        this.resetModal()
      },
      resetModal() {
        this.username = '';
        this.password = '';
        this.loginState = null
      },
      handleOk(bvModalEvt) {
        bvModalEvt.preventDefault();
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
</style>
