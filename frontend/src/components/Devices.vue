<template>
    <div class=".table-responsive m-3">
        <b-table responsive small  striped sort-icon-left hover scrollable 
            :items="locationDevices" 
            :fields="fields" 
            :sort-by.sync="sortBy" 
            :sort-desc.sync="sortDesc" 
            :tbody-tr-class="'pointer'"
            @row-clicked="clicked"
            head-variant="dark">
        </b-table>
    </div>
</template>

<script>


export default {
    name: 'Devices',
    props: ["locationDevices", "location"],
    data() {
        return {
            sortBy: "ping_code",
            sortDesc: true,
            selectMode: "single",
            fields: [
                {
                    key:'ping_code',
                    sortable: true,
                    label: 'Status',
                    tdClass: "ping_code_class",
                    thClass: "thead-dark"
                },
                {
                    key:'id',
                    sortable: true,
                    label:"ID"
                },
                {
                    key:'description',
                    sortable: true,
                    label:"Description"
                },
                {
                    key:'group',
                    sortable: true,
                    label:'Group'
                },
                {
                    key:'ip',
                    sortable: true,
                    label:"IP"
                },
                {
                    key:'ping_time',
                    sortable: true,
                    label:'Latency'
                },
                {
                    key:'time_stamp',
                    sortable: true,
                    label:'Last Checked',
                    formatter: 'get_time'
                },
                {
                    key:'lastup',
                    sortable: true,
                    label:'Last Up',
                    formatter: 'get_time'
                },
                { 
                    key:'os',
                    sortable: true,
                    label:"OS"
                },
                {
                    key:'version',
                    sortable: true,
                    label:"Version"
                },
                {
                    key:'attribute1',
                    sortable: true,
                    label:"Attribute1"
                },
                {
                    key:'attribute2',
                    sortable: true,
                    label:"Attribute2"
                },
                {
                    key:'attribute3',
                    sortable: true,
                    label:"Attribute3"
                },
                {
                    key:'attribute4',
                    sortable: true,
                    label:"Attribute4"
                },
                {
                    key:'attribute5',
                    sortable: true,
                    label:"Attribute5"
                },
                
            ]
        }
    },
    methods: {
        ping_code_class(value){
            if (value == 0){
                return "up"
            }
            else if (value == 1){
                return "dns"
            }
            else{
                return "down"
            }
        },
        get_time: function(static_time){
            if (static_time == null){
                return '-'
            }
            var relative_time = Math.round((Date.now() - Date.parse(static_time+'+0000')) / 60000)
            if (relative_time >= 60 && relative_time < 1440){
                relative_time = Math.round(relative_time / 60) + 'h'
            }
            else if (relative_time >= 1440){
                relative_time = Math.round(relative_time / 60 / 24) + 'd'
            }
            else {
                relative_time = relative_time + 'm'
            }
            return relative_time
        },
        clicked(item) {
            this.$emit("scan-device", item.id)
        }
    }
}
</script>

<style scoped>

</style>
