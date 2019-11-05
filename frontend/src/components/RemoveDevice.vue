<template>
  <div class="remove-device">
    <a v-on:click="show">Remove Device</a>
    <b-modal
      id="modal-prevent-closing"
      ref="modal"
      title="Remove Device"
      @show="resetModal"
      @hidden="resetModal"
      @ok="handleOk"
    >
      <form ref="form" @submit.stop.prevent="handleSubmit">
        <b-form-group
          :state="idState"
          invalid-feedback="ID is required"
        >
          <b-form-input
            id="id-add"
            v-model="id"
            :state="idState"
            required
          ></b-form-input>
        </b-form-group>
      </form>
    </b-modal>
  </div>
</template>

<script>
export default {
  name: 'RemoveDevice',
  props: {
  },
  data() {
      return {
          id: '',
          idState: null
      }
  },
  methods: {
      show(){
          this.$bvModal.show('modal-prevent-closing')
      },
      checkFormValidity() {
        const valid = this.$refs.form.checkValidity()
        this.idState = valid
        return valid
      },
      resetModal() {
        this.id = ''
        this.idState = null
      },
      handleOk(bvModalEvt) {
        bvModalEvt.preventDefault()
        this.handleSubmit()
      },
      handleSubmit() {
        if (!this.checkFormValidity()) {
          return
        }
        this.$emit("remove-device", this.id)

        this.$nextTick(() => {
          this.$bvModal.hide('modal-prevent-closing')
        })
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
