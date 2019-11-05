<template>
  <div class="modify-device modal-lg">
    <a v-on:click="show">Logs</a>
    <b-modal
      id="modal-logs"
      title="Logs"
      size="xl"
      scrollable
    >
        <pre class="my-4">
            {{ logs }}
        </pre>
    </b-modal>
  </div>
</template>

<script>
import Api from '@/services/api';

export default {
  name: 'Logs',
  props: {
  },
  data(){
      return {
          logs: ''
      }
  },
  methods: {
      show(){
          this.getLogs()
          this.$bvModal.show('modal-logs')
      },
      async getLogs(){
          let data = (await Api.getLogs()).reverse()
          this.logs = JSON.stringify(data, null, 2)
      }
  }
}
</script>

<style scoped>
  pre {
    white-space: pre-wrap;       /* Since CSS 2.1 */
    white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
    white-space: -pre-wrap;      /* Opera 4-6 */
    white-space: -o-pre-wrap;    /* Opera 7 */
    word-wrap: break-word;       /* Internet Explorer 5.5+ */
}
</style>
