<template>
  <div class="modify-device">
    <a v-on:click="show">Modify Device</a>
    <b-modal
      id="modal-modify-device"
      ref="modal"
      title="Modify Device"
      @show="resetModal"
      @hidden="hideModal"
      @ok="handleOk"
    >
      <form ref="form" @submit.stop.prevent="handleSubmit">
        <b-form-group
          :state="idState"
          invalid-feedback="ID is required"
        >
          <b-form-input class="mt-1"
            id="id-input"
            v-model="id"
            :state="idState"
            required
          ></b-form-input>
          <b-form-radio-group class="mt-1"
            id="radio-group-1"
            v-model="selected"
            :options="options"
            name="radio-options"
      ></b-form-radio-group>
        </b-form-group>
      </form>
    </b-modal>
  </div>
</template>

<script>
export default {
  name: 'ModifyDevice',
  props: {
  },
  data() {
      return {
          id: '',
          idState: null,
          selected: 'Add',
          options:[
              { text: "Add", value: 'Add'},
              { text: "Remove", value: 'Remove'}
          ]
      }
  },
  methods: {
      show(){
        this.$bvModal.show('modal-modify-device')
        this.$emit("pause-timer", true)
      },
      checkFormValidity() {
        const valid = this.$refs.form.checkValidity()
        this.idState = valid
        return valid
      },
      hideModal(){
        this.resetModal()
        this.$emit("pause-timer", false)
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
        this.$emit("modify-device", {id: this.id, modify: this.selected})

        this.$nextTick(() => {
          this.$bvModal.hide('modal-modify-device')
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
