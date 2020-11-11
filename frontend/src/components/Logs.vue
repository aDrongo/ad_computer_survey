<template>
  <div>
    <a v-on:click="show">Logs</a>
    <b-modal
      id="modal-logs"
      title="Logs"
      size="xl"
      @hidden="hideModal"
      hide-footer
    >
    <div class="row mr-auto ml-1">
      <b-form-group>
        <b-input-group size="sm">
          <b-form-input
            v-model="filter"
            type="search"
            id="filterInput"
            placeholder="Type to Search"
            debounce="500"
          ></b-form-input>
          <b-input-group-append>
            <b-button class="ml-1" :disabled="!filter" @click="filter = ''">Clear</b-button>
          </b-input-group-append>
        </b-input-group>
      </b-form-group>
    </div>
      <div class="table-responsive">
        <b-table responsive small striped sort-icon-left hover scrollable sticky-header selectable
            :items="logs" 
            :fields="fields" 
            :sort-by.sync="sortBy" 
            :sort-desc.sync="sortDesc"
            :filter="filter"
            :filter-included-fields="filterOn"
            @row-clicked="expandAdditionalInfo" 
            head-variant="dark">
            <template slot="row-details" slot-scope="row">
              <table class="table table-bordered table-sm no-pointer" style="width: 100%;">
                <thead class="thead-dark"><tr><th>New Value</th><th>Old Value</th></tr></thead>
                  <tbody><tr><td><pre>{{ row.item.new_values }}</pre></td><td><pre>{{ row.item.old_values }}</pre></td></tr></tbody>
              </table>
          </template>
        </b-table>
    </div>
    </b-modal>
  </div>
</template>

<script>
import Api from '@/services/api';

export default {
  name: 'Logs',
  data(){
        return {
            logs: null,
            filter: null,
            sortBy: "id",
            sortDesc: true,
            selectMode: "single",
            filterOn: ['device','time','id'],
            fields: [
                {
                  key: 'id',
                  sortable: true,
                  label: 'EventId',
                  sortByFormatted: true,
                  filterByFormatted: true
                },
                {
                    key:'time',
                    label: 'Time',
                    sortByFormatted: true,
                    filterByFormatted: true
                },
                {
                    key:'device',
                    sortable: true,
                    label:"Device",
                    sortByFormatted: true,
                    filterByFormatted: true
                }
            ]
        }
  },
  methods: {
      expandAdditionalInfo(row){
        row._showDetails = !row._showDetails;
      },
      show(){
        this.getLogs()
        this.$bvModal.show('modal-logs')
        this.$emit("pause-timer", true)
      },
      async getLogs(){
        this.logs = await Api.getLogs()
      },
      hideModal(){
        this.$emit("pause-timer", false)
      },
      format(data){
        JSON.stringify(data, null, 2)
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
